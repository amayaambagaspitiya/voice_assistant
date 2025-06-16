import sounddevice as sd
from scipy.io.wavfile import write
import whisper

class WhisperMic:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)

    def record(self, duration=6, filename="mic_input.wav"):
        fs = 16000  # Sample rate (16kHz recommended)
        print(f"Recording for {duration} seconds...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
        sd.wait()
        write(filename, fs, recording)
        print("Audio saved to", filename)
        return filename

    def transcribe(self, file_path):
        result = self.model.transcribe(file_path)
        return result["text"]
