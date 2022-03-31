#!/usr/bin/env bash

# this script make several assumptions:
#   you don't mind compiling and installing Python 3.9.7 to /usr/local/bin via `sudo make altinstall`
#   you don't mind installing the Nvidia CUDA toolkit version 10.2
#   user running this script has sudo privilege
#   you will run the application later as the user installing the script

#protonvpn=$1

mkdir -p $HOME/bin

# install software dependencies
sudo apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
sudo apt-get install -y python3-tkinter python3-dev scrot

# install Nvidia CUDA toolkit
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin --output-document=bin/cuda-ubuntu1804.pin
sudo mv bin/cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget http://developer.download.nvidia.com/compute/cuda/10.2/Prod/local_installers/cuda-repo-ubuntu1804-10-2-local-10.2.89-440.33.01_1.0-1_amd64.deb --output-document=bin/cuda-repo-ubuntu1804-10-2-local-10.2.89-440.33.01_1.0-1_amd64.deb
sudo dpkg -i bin/cuda-repo-ubuntu1804-10-2-local-10.2.89-440.33.01_1.0-1_amd64.deb
sudo apt-key add /var/cuda-repo-10-2-local-10.2.89-440.33.01/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda

# install python 3.9.7 and dependencies
wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz --output-document=bin/Python-3.9.7.tgz
cd bin || exit
tar -xf Python-3.9.7.tgz
cd Python-3.9.7 || exit
./configure --enable-optimizations && \
make -j 4 && \
sudo make altinstall && \
cd ../.. || exit
python3.9 -V || exit

# install ycm requirements, build Cython modules, and init protonvpn IF parameter was set
pip3.9 install -r requirements.txt && \
python3.9 setup.py build_ext --inplace
#if [$protonvpn == "vpn"]
#then
#  sudo protonvpn init
#fi

# install sdkman!
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install java 11.0.7.hs-adpt

# install RuneLite
wget https://github.com/runelite/launcher/releases/download/2.4.2/RuneLite.jar --output-document=$HOME/bin/RuneLite.jar
