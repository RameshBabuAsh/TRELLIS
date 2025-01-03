from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
import os
import shutil
from pathlib import Path
from PIL import Image
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from OmniGen import OmniGenPipeline # type: ignore
import sys
from pyngrok import ngrok
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Load OmniGen pipeline
pipe = OmniGenPipeline.from_pretrained("Shitao/OmniGen-v1")

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

@app.post("/generate-image")
async def generate_image(
    product_name: str = Form(...),
    message_number: int = Form(...),
    prompt: str = Form(...),
    image: UploadFile = File(None),  # Make image optional
    guidance_scale: float = Form(...),
    img_guidance_scale: float = Form(None)  # Optional when using prompt only
):
    try:
        # Create a unique folder in Google Drive
        folder_metadata = {
            'name': f"{product_name}_{message_number}",
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')

        # If an image is provided, use it; otherwise, use only the prompt
        if image:
            # Save the input image locally
            input_image_path = f"/tmp/input_image.jpg"
            with open(input_image_path, "wb") as f:
                shutil.copyfileobj(image.file, f)

            # Generate image using OmniGen pipeline with input image
            images = pipe(
                prompt=prompt,
                input_images=[input_image_path],
                height=256,
                width=256,
                separate_cfg_infer=True,
                guidance_scale=guidance_scale,
                img_guidance_scale=img_guidance_scale,
                max_input_image_size=768,
                seed=1
            )
        else:
            # Generate image using OmniGen pipeline with prompt only
            images = pipe(
                prompt=prompt,
                height=256,
                width=256,
                guidance_scale=guidance_scale,
                separate_cfg_infer=True,
                seed=0
            )

        # Save output image locally
        output_image_path = "/tmp/output_image.png"
        images[0].save(output_image_path)

        # Upload input and output images to Google Drive
        if image:
            upload_to_drive(input_image_path, folder_id, drive_service)
        upload_to_drive(output_image_path, folder_id, drive_service)

        # Make the folder public
        make_folder_public(folder_id, drive_service)

        return JSONResponse({
            "message": "Image generated successfully",
            "drive_folder_id": folder_id
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
