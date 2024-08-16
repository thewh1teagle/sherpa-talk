import sherpa_onnx

class TextDecoder:
    def __init__(self, encoder, decoder, tokens) -> None:
        self.recognizer = sherpa_onnx.OfflineRecognizer.from_whisper(
         encoder=encoder,
         decoder=decoder,
         tokens=tokens,
         num_threads=1,
         decoding_method='greedy_search',
         debug=False,
         language='en',
         task='transcribe',
         tail_paddings=-1   
        )
    def get_text(self, sample_rate, samples):
        s = self.recognizer.create_stream()
        s.accept_waveform(sample_rate, samples)
        self.recognizer.decode_stream(s)
        return s.result.text
        
        