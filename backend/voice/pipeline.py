from voice.asr import transcribe
from dialogue.extract_profile import extract_profile
from recommender.recommend import recommend
from database.db import save_conversation
from voice.tts import speak_recommendation

def process_voice_input(audio_path):
    conversation_text = transcribe(audio_path)
    profile = extract_profile(conversation_text)
    recommendations = recommend(profile)
    save_conversation(conversation_text, profile, recommendations)
    speech_result = speak_recommendation(profile, recommendations)

    return {
        "transcribed_text": conversation_text,
        "extracted_profile": profile,
        "recommendations": recommendations,
        "response_audio_path": speech_result["audio_path"],
        "response_text_hindi": speech_result["hindi_response"],
        "response_text_english": speech_result["english_response"]
    }