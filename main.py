from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
import os
import shutil
from pathlib import Path
import imageio
from PIL import Image
from io import BytesIO
import uvicorn
from pyngrok import ngrok
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import sys

from trellis.pipelines import TrellisImageTo3DPipeline
from trellis.utils import render_utils, postprocessing_utils

# Set environment variables
os.environ['ATTN_BACKEND'] = 'xformers'   # Can be 'flash-attn' or 'xformers', default is 'flash-attn'
os.environ['SPARSE_ATTN_BACKEND'] = 'xformers'
os.environ['SPCONV_ALGO'] = 'native'        # Can be 'native' or 'auto', default is 'auto'.
                                            # 'auto' is faster but will do benchmarking at the beginning.
                                            # Recommended to set to 'native' if run only once.

# Load a pipeline from a model folder or a Hugging Face model hub.
pipeline = TrellisImageTo3DPipeline.from_pretrained("JeffreyXiang/TRELLIS-image-large")
pipeline.cuda()

# Initialize FastAPI app
app = FastAPI()

# Helper function to upload files to Google Drive
def upload_to_drive(file_path, folder_id, drive_service):
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

def make_folder_public(folder_id, drive_service):
    """Set the sharing permissions of a folder to public."""
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    drive_service.permissions().create(
        fileId=folder_id,
        body=permission,
        fields='id'
    ).execute()

@app.get("/")
async def root():
    return JSONResponse({"message": "Welcome to the 3D asset generation API"})

@app.post("/generate-3d")
async def generate_3d(
    product_name: str = Form(...),
    message_number: int = Form(...),
    image: UploadFile = File(...),
):
    try:
        # Create a unique folder in Google Drive
        folder_metadata = {
            'name': f"{product_name}_{message_number}",
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')

        # Save the input image locally
        input_image_path = f"/tmp/input_image.jpg"
        with open(input_image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

        # Open the saved image using PIL
        pil_image = Image.open(input_image_path)

        # Run the Trellis pipeline
        outputs = pipeline.run(
            pil_image,
            seed=1,
        )

        # Render outputs and save locally
        gaussian_video = render_utils.render_video(outputs['gaussian'][0])['color']
        radiance_field_video = render_utils.render_video(outputs['radiance_field'][0])['color']
        mesh_video = render_utils.render_video(outputs['mesh'][0])['normal']

        gaussian_path = "/tmp/gaussian.mp4"
        radiance_field_path = "/tmp/radiance_field.mp4"
        mesh_path = "/tmp/mesh.mp4"

        imageio.mimsave(gaussian_path, gaussian_video, fps=30)
        imageio.mimsave(radiance_field_path, radiance_field_video, fps=30)
        imageio.mimsave(mesh_path, mesh_video, fps=30)

        # Upload videos to Google Drive
        upload_to_drive(gaussian_path, folder_id, drive_service)
        upload_to_drive(radiance_field_path, folder_id, drive_service)
        upload_to_drive(mesh_path, folder_id, drive_service)

        # Save GLB file
        glb_path = "/tmp/output.glb"
        glb = postprocessing_utils.to_glb(
            outputs['gaussian'][0],
            outputs['mesh'][0],
            simplify=0.95,
            texture_size=1024,
        )
        glb.export(glb_path)

        # Upload GLB file to Google Drive
        upload_to_drive(glb_path, folder_id, drive_service)

        # Save Gaussians as PLY files
        ply_path = "/tmp/output.ply"
        outputs['gaussian'][0].save_ply(ply_path)

        # Upload PLY file to Google Drive
        upload_to_drive(ply_path, folder_id, drive_service)

        make_folder_public(folder_id, drive_service)

        return JSONResponse({
            "message": "3D assets generated successfully",
            "drive_folder_id": folder_id,
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <ngrok_auth_token> <service_account_file_path>")
        sys.exit(1)
    
    ngrok_auth_token = sys.argv[1]
    service_account_file_path = sys.argv[2]

    # Google Drive setup
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    credentials = Credentials.from_service_account_file(service_account_file_path, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=credentials)

    port_no = 5000
    ngrok.set_auth_token(ngrok_auth_token)
    public_url = ngrok.connect(port_no).public_url
    print(f"To access the global link, please click {public_url}")

    uvicorn.run(app, host="0.0.0.0", port=port_no)
