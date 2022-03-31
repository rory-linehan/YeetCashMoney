#!/usr/bin/env bash

# assumes clean install of Ubuntu 18.04

# install software package dependencies
#sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y build-essential git cmake wget openvpn openssl-dev dialog libgirepository1.0-dev unzip zip
sudo apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

# seed directories
mkdir -p bin/
mkdir -p bot/ml/vision/models/

# install nvidia drivers and dependencies
# Add NVIDIA package repositories
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-repo-ubuntu1804_10.1.243-1_amd64.deb \
--output-document=bin/cuda-repo-ubuntu1804_10.1.243-1_amd64.deb
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
sudo dpkg -i bin/cuda-repo-ubuntu1804_10.1.243-1_amd64.deb
sudo apt-get update
wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb \
--output-document=bin/nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo apt install ./bin/nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo apt-get update

# Install NVIDIA driver
sudo apt-get install --no-install-recommends nvidia-driver-430
echo "Reboot. Check that GPUs are visible using the command: nvidia-smi"
sudo reboot
nvidia-smi

# Install development and runtime libraries (~4GB)
sudo apt-get install --no-install-recommends \
    cuda-10-0 \
    libcudnn7=7.6.4.38-1+cuda10.0  \
    libcudnn7-dev=7.6.4.38-1+cuda10.0

# Install TensorRT. Requires that libcudnn7 is installed above.
sudo apt-get install -y --no-install-recommends libnvinfer6=6.0.1-1+cuda10.0 \
    libnvinfer-dev=6.0.1-1+cuda10.0 \
    libnvinfer-plugin6=6.0.1-1+cuda10.0

sudo apt update && sudo apt upgrade -y

# install gdrive
#wget https://github.com/gdrive-org/gdrive/releases/download/2.1.0/gdrive-linux-x64 --output-document=bin/gdrive
#sudo chmod +x bin/gdrive

# install pretrained YOLOv3 model from:
#gdrive download https://drive.google.com/file/d/1tIwRa9ifuLK00aXnbkMGcH4WaSv-eNuL
#cp backend.h5 ml/vision/models/backend.h5

# install forked keras-yolo3
cd ml/vision/src || exit
git clone git@github.com:rory-linehan/keras-yolo3.git
mv keras-yolo3 keras_yolo3
cd ..

# install forked labelImg and dependencies
cd ml/vision/src || exit
git clone git@github.com:rory-linehan/labelImg.git
cd labelImg || exit
sudo apt-get install pyqt5-dev-tools && \
sudo pip3.7 install -r requirements/requirements-linux-python3.txt && \
make qt5py3

# install additional components
# tensorflow docker image
docker pull tensorflow/tensorflow:latest-py3
