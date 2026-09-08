import whisper

model = whisper.load_model("small")

result = model.transcribe("voice/sample_audio.mp3", language="hi", task="translate")

print("Translated text (English):")
print(result["text"])