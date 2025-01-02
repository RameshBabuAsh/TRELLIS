const fs = require('fs');
const FormData = require('form-data');
const path = require('path');

async function testGenerate3D() {
    const fetch = (await import('node-fetch')).default;
    const formData = new FormData();
    formData.append('product_name', 'Test Product');
    formData.append('message_number', 123);
    formData.append('image', fs.createReadStream(path.join(__dirname, 'large.jpg')));

    try {
        const response = await fetch('https://9842-34-74-54-249.ngrok-free.app/generate-3d', {
            method: 'POST',
            body: formData,
            headers: {
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
