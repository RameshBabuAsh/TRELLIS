<img src="assets/logo.webp" width="100%" align="center">
<h1 align="center">Structured 3D Latents<br>for Scalable and Versatile 3D Generation</h1>
<p align="center"><a href="https://arxiv.org/abs/2412.01506"><img src='https://img.shields.io/badge/arXiv-Paper-red?logo=arxiv&logoColor=white' alt='arXiv'></a>
<a href='https://trellis3d.github.io'><img src='https://img.shields.io/badge/Project_Page-Website-green?logo=googlechrome&logoColor=white' alt='Project Page'></a>
<a href='https://huggingface.co/spaces/JeffreyXiang/TRELLIS'><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Live_Demo-blue'></a>
</p>
<p align="center"><img src="assets/teaser.png" width="100%"></p>

<span style="font-size: 16px; font-weight: 600;">T</span><span style="font-size: 12px; font-weight: 700;">RELLIS</span> is a large 3D asset generation model. It takes in text or image prompts and generates high-quality 3D assets in various formats, such as Radiance Fields, 3D Gaussians, and meshes. The cornerstone of <span style="font-size: 16px; font-weight: 600;">T</span><span style="font-size: 12px; font-weight: 700;">RELLIS</span> is a unified Structured LATent (<span style="font-size: 16px; font-weight: 600;">SL</span><span style="font-size: 12px; font-weight: 700;">AT</span>) representation that allows decoding to different output formats and Rectified Flow Transformers tailored for <span style="font-size: 16px; font-weight: 600;">SL</span><span style="font-size: 12px; font-weight: 700;">AT</span> as the powerful backbones. We provide large-scale pre-trained models with up to 2 billion parameters on a large 3D asset dataset of 500K diverse objects. <span style="font-size: 16px; font-weight: 600;">T</span><span style="font-size: 12px; font-weight: 700;">RELLIS</span> significantly surpasses existing methods, including recent ones at similar scales, and showcases flexible output format selection and local 3D editing capabilities which were not offered by previous models.

<!-- Why This Repository -->
## 🤔 Why This Repository

Many people don't have the resources to run TRELLIS on their local systems, so they use Kaggle or Colab. This repository is a modified version for Kaggle or Colab implementation. Users can use the commands in `runner.txt` to get their own Kaggle/Colab version of TRELLIS. A sample FastAPI is implemented in `main.py`, which users can customize in whatever way they want. Additionally, `test.js` contains a sample POST request for testing purposes.

<!-- Features -->
## 🌟 Features
- **High Quality**: It produces diverse 3D assets at high quality with intricate shape and texture details.
- **Versatility**: It takes text or image prompts and can generate various final 3D representations including but not limited to *Radiance Fields*, *3D Gaussians*, and *meshes*, accommodating diverse downstream requirements.
- **Flexible Editing**: It allows for easy editings of generated 3D assets, such as generating variants of the same object or local editing of the 3D asset.


