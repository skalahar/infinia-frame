Installation Procedure


1. Install this git
  - git clone https://github.com/skalahar/infinia-frame.git


2. Install the virtual environment
  - python3 -m venv .venv
  - Install Pillow (pip install pillow)
  - Install OpenCV (pip install opencv-contrib-python)
  - install inky (pip install inky[rpi]==1.5.0)


3. get XNNPACK 
  - git clone https://github.com/google/XNNPACK.git
  - cd XNNPACK
  - git checkout 1c8ee1b68f3a3e0847ec3c53c186c5909fa3fbd3
  - mkdir build
  - cd build
  - cmake -DXNNPACK_BUILD_TESTS=OFF -DXNNPACK_BUILD_BENCHMARKS=OFF ..
  - cmake --build . --config Release

 
4. get OnnxStream
  - git clone https://github.com/vitoplantamura/OnnxStream.git
  - cd OnnxStream
  - cd src
  - mkdir build
  - cd build
  - cmake -DMAX_SPEED=ON -DOS_LLM=OFF -DOS_CUDA=OFF -DXNNPACK_DIR="${INSTALL_DIR}/XNNPACK" ..
  - cmake --build . --config Release


5. get the models
  - mkdir models
  - cd models
  - git clone --depth=1 https://huggingface.co/vitoplantamura/stable-diffusion-xl-turbo-1.0-anyshape-onnxstream
