import sherpa_onnx
import sounddevice as sd
import os
import sys
from loguru import logger

class MicRecognizer:
    def __init__(self, silero_vad_model) -> None:
        self.silero_vad_model = silero_vad_model
    
    def get_speech(self, mic_sample_rate = 16000):
        if "SHERPA_ONNX_MIC_SAMPLE_RATE" in os.environ:
            mic_sample_rate = int(os.environ.get("SHERPA_ONNX_MIC_SAMPLE_RATE"))
            logger.info(f"Change microphone sample rate to {mic_sample_rate}")

        sample_rate = 16000
        samples_per_read = int(0.1 * sample_rate)  # 0.1 second = 100 ms

        config = sherpa_onnx.VadModelConfig()
        config.silero_vad.model = self.silero_vad_model
        config.sample_rate = sample_rate

        vad = sherpa_onnx.VoiceActivityDetector(config, buffer_size_in_seconds=30)

        # python3 -m sounddevice
        # can also be used to list all devices

        devices = sd.query_devices()
        if len(devices) == 0:
            logger.error("No microphone devices found")
            logger.error(
                "If you are using Linux and you are sure there is a microphone "
                "on your system, please use "
                "./vad-alsa.py"
            )
            sys.exit(0)

        logger.info(devices)

        if "SHERPA_ONNX_MIC_DEVICE" in os.environ:
            input_device_idx = int(os.environ.get("SHERPA_ONNX_MIC_DEVICE"))
            sd.default.device[0] = input_device_idx
            logger.info(f'Use selected device: {devices[input_device_idx]["name"]}')
        else:
            input_device_idx = sd.default.device[0]
            logger.info(f'Use default device: {devices[input_device_idx]["name"]}')

        logger.info("Started! Please speak. Press Ctrl C to exit")

        printed = False
        k = 0
        try:
            with sd.InputStream(
                channels=1, dtype="float32", samplerate=mic_sample_rate
            ) as s:
                while True:
                    samples, _ = s.read(samples_per_read)  # a blocking read
                    samples = samples.reshape(-1)

                    if mic_sample_rate != sample_rate:
                        import librosa

                        samples = librosa.resample(
                            samples, orig_sr=mic_sample_rate, target_sr=sample_rate
                        )

                    vad.accept_waveform(samples)

                    if vad.is_speech_detected() and not printed:
                        logger.info("Detected speech")
                        printed = True

                    if not vad.is_speech_detected():
                        printed = False

                    while not vad.empty():
                        
                        samples = vad.front.samples
                        yield samples

                        vad.pop()
        except KeyboardInterrupt:
            logger.info("\nCaught Ctrl + C. Exit")
