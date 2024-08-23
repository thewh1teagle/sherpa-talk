from pywhispercpp.model import Model
import numpy as np

class TextDecoder:
    def __init__(self, model_path: str) -> None:
        self.model = Model(model_path)
    def get_text(self, _sample_rate, samples: np.array):
        segments = self.model.transcribe(samples)
        text = ' '.join(s.text for s in segments)
        return text
        
