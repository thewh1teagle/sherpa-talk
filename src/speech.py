import sherpa_onnx
import sounddevice as sd
from loguru import logger
import pyttsx3

class SpeechCreator:
    def __init__(self, vits_model, vits_lexicon, vits_tokens) -> None:
        self.tts = pyttsx3.init()
    
    def create(self, text, sid = 0, speed = 1.0, play = False):
        logger.debug("Create Speech")
        self.tts.say(text)
        self.tts.runAndWait()
        logger.debug("Done create speech")