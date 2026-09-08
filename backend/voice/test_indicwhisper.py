from transformers import pipeline
import librosa

transcriber = pipeline(
    "automatic-speech-recognition",
    model="ai4bharat/indicwav2vec-hindi"
)

def transcribe(audio_path):
    audio, sr = librosa.load(audio_path, sr=16000)
    result = transcriber(audio)
    return result["text"]

if __name__ == "__main__":
    text = transcribe("sample_audio.mp3")
    print("Transcribed text:")
    print(text)