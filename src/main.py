from record import SpeechRecognizer
from transcribe import TextDecoder
from speech import SpeechCreator
from agent import Agent
import config


def main():
    speech_recognizer = SpeechRecognizer(config.silero_vad_model)
    text_decoder = TextDecoder(model_path=config.whisper_model_path)
    speech_creator = SpeechCreator(vits_model=config.vits_model, vits_lexicon=config.vits_lexicon, vits_tokens=config.vits_tokens)
    agent = Agent(model_path=config.think_model_path)        

    for speech in speech_recognizer.speech_iter(mic_sample_rate=config.sample_rate):
        text = text_decoder.get_text(config.sample_rate, speech)
        if not text:
            continue
        answer = agent.ask(prompt=text)
        speech_creator.create(answer, play=True) 
        

if __name__ == "__main__":
    main()