nvcc --version 

wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sudo sh cuda_11.8.0_520.61.05_linux.run --silent --toolkit

export DEBIAN_FRONTEND=noninteractive
export CUDA_HOME=/usr/local/cuda
export PATH=${CUDA_HOME}/bin:${PATH}
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}
export TORCH_CUDA_ARCH_LIST="7.0;7.5;8.0;8.6+PTX"
export FORCE_CUDA=1

pip uninstall pandas-gbq -y

# Update and install system dependencies
echo "Updating system and installing dependencies..."
apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3-pip \
    wget \
    git \
    ninja-build \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.10 as the default Python version
echo "Setting Python 3.10 as default..."
update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Upgrade pip, setuptools, and wheel
echo "Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel

echo "Environment setup completed."

nvcc --version

pip uninstall torch torchvision torchaudio -y

pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu118

pip install pillow imageio imageio-ffmpeg tqdm easydict opencv-python-headless scipy ninja rembg onnxruntime trimesh xatlas pyvista pymeshfix igraph transformers
pip install git+https://github.com/EasternJournalist/utils3d.git@9a4eb15e4021b67b12c460c7057d642626897ec8

pip install xformers==0.0.27.post2 --index-url https://download.pytorch.org/whl/cu118

pip install kaolin -f https://nvidia-kaolin.s3.us-east-2.amazonaws.com/torch-2.4.0_cu121.html

mkdir -p /tmp/extensions && \
    git clone https://github.com/NVlabs/nvdiffrast.git /tmp/extensions/nvdiffrast && \
    pip install /tmp/extensions/nvdiffrast

mkdir -p /tmp/extensions && \
    git clone --recurse-submodules https://github.com/JeffreyXiang/diffoctreerast.git /tmp/extensions/diffoctreerast && \
    pip install /tmp/extensions/diffoctreerast

mkdir -p /tmp/extensions && \
    git clone https://github.com/autonomousvision/mip-splatting.git /tmp/extensions/mip-splatting2 && \
    pip install /tmp/extensions/mip-splatting2/submodules/diff-gaussian-rasterization/

pip install spconv-cu118

pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

pip install annotated-types==0.7.0 anyio==4.7.0 click==8.1.8 colorama==0.4.6 exceptiongroup==1.2.2 fastapi==0.115.6 h11==0.14.0 idna==3.10 pydantic==2.10.4

pip install pydantic_core==2.27.2 pyngrok==7.2.2 PyYAML==6.0.2 sniffio==1.3.1 starlette==0.41.3 typing_extensions==4.12.2 uvicorn==0.34.0

export CUDA_HOME="/usr/local/cuda-11.8"
export PATH="$CUDA_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$CUDA_HOME/lib64:${LD_LIBRARY_PATH:-}"

# Check if CUDA is correctly set up
echo "Checking CUDA version:"
nvcc --version

echo "Checking if libnvrtc is available:"
ldconfig -p | grep libnvrtc

# Verify the availability of required libraries
echo "Verifying required libraries:"
if ldconfig -p | grep -q "libnvrtc-builtins.so.11.8"; then
    echo "CUDA libraries loaded successfully."
else
    echo "Error loading CUDA libraries: libnvrtc-builtins.so.11.8 not found."
    exit 1
fi