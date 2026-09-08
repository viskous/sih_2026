from gtts import gTTS
import uuid
from dialogue.providers.gemini_provider import call_llm

def generate_response_text(profile, recommendations):
    prompt = """You are a friendly voice assistant helping someone find suitable job training.
Given their profile and the recommended trades below, write a short, natural, conversational 
response (2-4 sentences) explaining the recommendation as if speaking directly to them. 
Be warm and encouraging. Don't just list data — explain why it fits them.
Output ONLY the response text, nothing else."""

    context = f"Profile: {profile}\nRecommendations: {recommendations}"
    response_text = call_llm(prompt, context)
    return response_text

def translate_to_hindi(english_text):
    prompt = "Translate the following text to natural, conversational Hindi. Output ONLY the Hindi translation, nothing else."
    hindi_text = call_llm(prompt, english_text)
    return hindi_text

def synthesize(text, output_dir="voice/output"):
    filename = f"{output_dir}/response_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang="hi")
    tts.save(filename)
    return filename

def speak_recommendation(profile, recommendations, output_dir="voice/output"):
    english_response = generate_response_text(profile, recommendations)
    hindi_response = translate_to_hindi(english_response)
    audio_path = synthesize(hindi_response, output_dir)
    return {
        "english_response": english_response,
        "hindi_response": hindi_response,
        "audio_path": audio_path
    }