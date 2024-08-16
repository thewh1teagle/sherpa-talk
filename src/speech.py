import sherpa_onnx
import sounddevice as sd
from loguru import logger

class SpeechCreator:
    def __init__(self, vits_model, vits_lexicon, vits_tokens) -> None:
        tts_config = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model=vits_model,
                lexicon=vits_lexicon,
                data_dir='',
                dict_dir='',
                tokens=vits_tokens,
            ),
            debug=False,
            num_threads=1,
            ),
            rule_fsts='',
            max_num_sentences=2,
        )
        if not tts_config.validate():
            raise ValueError("Please check your config")
        self.tts = sherpa_onnx.OfflineTts(tts_config)
    
    def create(self, text, sid = 0, speed = 1.0, play = False):
        logger.debug("Create Speech")
        audio = self.tts.generate(text, sid=sid, speed=speed)
        logger.debug("Done create speech")
        if play:
            self.play(audio)
        return audio

    def play(self, audio):
        sd.play(audio.samples, samplerate=audio.sample_rate)
        sd.wait()