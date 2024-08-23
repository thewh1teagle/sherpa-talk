# sherpa-talk

Voice assistant based on sherpa-onnx

## Setup

### Prepare [Vulkan](https://vulkan.lunarg.com/) SDK


*In Windows*
set the env `VULKAN_SDK` to `C:\VulkanSDK\<version>`.

*In macOS*
You can set `GGML_VULKAN=OFF`

*In Linux*

```console
sudo apt-get install libportaudio2
```

2. Prepare models
wget https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin

wget https://huggingface.co/unsloth/gemma-2-it-GGUF/resolve/main/gemma-2-2b-it.q2_k.gguf

mkdir vits-ljs
wget https://huggingface.co/csukuangfj/vits-ljs/resolve/main/vits-ljs.onnx -O vits-ljs/vits-ljs.onnx
wget https://huggingface.co/csukuangfj/vits-ljs/resolve/main/lexicon.txt -O vits-ljs/lexicon.txt
wget https://huggingface.co/csukuangfj/vits-ljs/resolve/main/tokens.txt -O vits-ljs/tokens.txt

3. Install dependencies

```console
CMAKE_ARGS="-DGGML_VULKAN=ON" pip install llama-cpp-python
git clone --recursive https://github.com/thewh1teagle/pywhispercpp -b feat/vulkan
CMAKE_ARGS="-DGGML_VULKAN=ON GGML_CCACHE=OFF" pip install ./pywhispercpp
pip install -r requirements.txt
```

4. Execute the program

```console
python3 src/main.py
```