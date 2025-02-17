Edit /etc/dphys-swapfile (e.g. sudo vim /etc/dphys-swapfile) and change the value of CONF_SWAPSIZE to 1024. You might be able to get away with a smaller swap size but it's been reported that the build process stalls with a swap size of 256.

Then restart swap with sudo /etc/init.d/dphys-swapfile restart

sudo apt-get update
sudo apt-get upgrade
sudo apt-get -y install tmux vim
sudo apt-get -y install cmake
sudo apt-get -y install python3-dev python3-venv python3-pip
sudo apt-get -y install imagemagick
sudo apt-get -y install git git-lfs
sudo apt-get -y install libopencv-dev  python3-opencv

git clone https://github.com/skalahar/infinia-frame.git

cd /home/skalahar/infinia-frame
python3 -m venv .venv
source .venv/bin/activate

python -m pip install opencv_contrib_python
python -m pip install inky[rpi]==1.5.0
python -m pip install pillow
python -m pip install flask
python -m pip install flask-socketio
  
# Following instructions taken directly from [OnnxStream repo](https://github.com/vitoplantamura/OnnxStream).

cd /home/skalahar/infinia-frame
git clone https://github.com/google/XNNPACK.git
cd XNNPACK
git checkout 1c8ee1b68f3a3e0847ec3c53c186c5909fa3fbd3
mkdir build
cd build
cmake -DXNNPACK_BUILD_TESTS=OFF -DXNNPACK_BUILD_BENCHMARKS=OFF ..
cmake --build . --config Release
 
cd /home/skalahar/infinia-frame
git clone https://github.com/vitoplantamura/OnnxStream.git
cd OnnxStream
cd src
mkdir build
cd build
cmake -DMAX_SPEED=ON -DOS_LLM=OFF -DOS_CUDA=OFF -DXNNPACK_DIR=/home/skalahar/infinia-frame/XNNPACK ..
cmake --build . --config Release

cd /home/skalahar/infinia-frame
mkdir models
cd models
git clone --depth=1 https://huggingface.co/vitoplantamura/stable-diffusion-xl-turbo-1.0-anyshape-onnxstream
