import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import speech_recognition as sr


class WhisperMic:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)


    def record(self, filename="mic_input.wav"):
        recognizer = sr.Recognizer()
        mic = sr.Microphone(sample_rate=16000)

        print("Listening... Speak now. Recording will auto-stop when you stop speaking.")

        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)

        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())

        print(f"Audio saved to {filename}")
        return filename


    def transcribe(self, file_path):
        result = self.model.transcribe(file_path)
        return result["text"]
