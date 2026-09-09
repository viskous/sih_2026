from fastapi import FastAPI
from pydantic import BaseModel
from recommender.recommend import recommend
from dialogue.extract_profile import extract_profile
from database.db import init_db, save_conversation
from database.db import init_db, save_conversation, get_dashboard_data
from fastapi import FastAPI, UploadFile, File
import shutil
from voice.asr import transcribe
from voice.pipeline import process_voice_input
from fastapi import Form
import requests
import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from fastapi import Response

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
app = FastAPI()
init_db()

class Profile(BaseModel):
    education_level: str
    existing_skills: list[str]
    interests: list[str]
    employment_preference: str
    mobility_constraint: bool
    region: str

class ConversationInput(BaseModel):
    conversation_text: str

@app.post("/recommend")
def get_recommendations(profile: Profile):
    results = recommend(profile.dict())
    return {"profile": profile.dict(), "recommendations": results}

@app.post("/converse")
def process_conversation(input: ConversationInput):
    profile = extract_profile(input.conversation_text)
    results = recommend(profile)
    save_conversation(input.conversation_text, profile, results)
    return {"extracted_profile": profile, "recommendations": results}

@app.get("/dashboard-data")
def dashboard_data():
    return get_dashboard_data()


@app.post("/voice-converse")
def voice_converse(audio: UploadFile = File(...)):
    temp_path = f"voice/temp_{audio.filename}"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    result = process_voice_input(temp_path)
    return result

@app.post("/whatsapp-webhook")
async def whatsapp_webhook(
    From: str = Form(...),
    NumMedia: str = Form(...),
    MediaUrl0: str = Form(None),
    MediaContentType0: str = Form(None)
):
    if int(NumMedia) == 0 or MediaUrl0 is None:
        resp = MessagingResponse()
        resp.message("Please send a voice note describing your background and skills.")
        return Response(content=str(resp), media_type="application/xml")

    # download the incoming voice note (needs Twilio auth)
    audio_response = requests.get(MediaUrl0, auth=(TWILIO_SID, TWILIO_TOKEN))
    temp_path = f"voice/temp_incoming_{From.replace(':', '_')}.ogg"
    with open(temp_path, "wb") as f:
        f.write(audio_response.content)

    # run the full pipeline
    result = process_voice_input(temp_path)

    # reply with text for now (audio reply needs a public URL, next step)
    resp = MessagingResponse()
    resp.message(result["response_text_english"])
    return Response(content=str(resp), media_type="application/xml")