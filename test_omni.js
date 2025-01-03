const fs = require('fs');
const path = require('path');
const FormData = require('form-data');

async function testGenerate3D() {
    const fetch = (await import('node-fetch')).default;
    const formData = new FormData();
    formData.append('product_name', 'Test Product');
    formData.append('message_number', '123');
    // formData.append('prompt', "In the <img><|image_1|></img>, do the changes: Replace the wheels with larger, sportier rims. Tint the windows. Replace the side mirrors with sleeker designs.")
    formData.append('prompt', 'a car with a sporty look and a dark tinted window');
    // formData.append('image', fs.createReadStream(path.join(__dirname, '1.485.jpg')));
    formData.append('guidance_scale', '3.3');
    // formData.append('img_guidance_scale', '1.6');

    try {
        const response = await fetch('https://4fc2-34-91-215-213.ngrok-free.app/generate-image', {
            method: 'POST',
            body: formData,
            headers: {
                ...formData.getHeaders(),
                'ngrok-skip-browser-warning': 'true'
            }
        });

        const data = await response.json();

        if (response.ok) {
            console.log('3D assets generated successfully.');
            console.log('Google Drive Folder ID:', data.drive_folder_id);
            console.log('View Files:', `https://drive.google.com/drive/folders/${data.drive_folder_id}`);
        } else {
            console.error('Error:', data.error);
        }
    } catch (error) {
        console.error('Error:', error.message);
    }
}

testGenerate3D();