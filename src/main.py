"""
1. Download Ollama from https://ollama.com/download and prepare llama3.1
ollama run llama3.1

3. Prepare sherpa models
wget https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx
wget https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.en.tar.bz2
tar xf sherpa-onnx-whisper-small.en.tar.bz2

mkdir vits-ljs
wget https://huggingface.co/csukuangfj/vits-ljs/resolve/main/vits-ljs.onnx -O vits-ljs/vits-ljs.onnx
wget https://huggingface.co/csukuangfj/vits-ljs/resolve/main/lexicon.txt -O vits-ljs/lexicon.txt
wget https://huggingface.co/csukuangfj/vits-ljs/resolve/main/tokens.txt -O vits-ljs/tokens.txt

4. Install dependencies
pip install -r requirements.txt

5. Execute the program
python3 src/main.py --silero-vad-model silero_vad.onnx
"""


from record import MicRecognizer
from transcribe import TextDecoder
from speech import SpeechCreator
from think import ThinkModel
import config

def main():
    mic_recognizer = MicRecognizer(config.silero_vad_model)
    text_decoder = TextDecoder(encoder=config.whisper_encoder, decoder=config.whisper_decoder, tokens=config.whisper_tokens)
    speech_creator = SpeechCreator(vits_model=config.vits_model, vits_lexicon=config.vits_lexicon, vits_tokens=config.vits_tokens)
    thinker = ThinkModel(model=config.think_model)        

    for speech in mic_recognizer.speech_iter(mic_sample_rate=config.sample_rate):
        text = text_decoder.get_text(config.sample_rate, speech)
        answer = thinker.ask(prompt=text)
        speech_creator.create(answer, play=True) 
        

if __name__ == "__main__":
    main()