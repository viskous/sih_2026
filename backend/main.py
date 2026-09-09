from fastapi import FastAPI, UploadFile, File, Response, Request
from pydantic import BaseModel
from recommender.recommend import recommend
from dialogue.extract_profile import extract_profile
from database.db import init_db, save_conversation
from database.db import init_db, save_conversation, get_dashboard_data
from fastapi import FastAPI, UploadFile, File
import shutil
from voice.asr import transcribe
from voice.pipeline import process_voice_input
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/audio", StaticFiles(directory="voice/output"), name="audio")
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

VERIFY_TOKEN = "any_random_string_you_pick"  # you'll enter this same value in Meta's dashboard

@app.get("/whatsapp-webhook")
def verify_webhook(request: Request):
    params = request.query_params
    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params.get("hub.challenge"))
    return Response(status_code=403)

@app.post("/whatsapp-webhook")
async def receive_whatsapp_message(request: Request):
    body = await request.json()
    # we'll parse the incoming message structure here next
    print(body)  # temporary, just to see what Meta actually sends
    return {"status": "received"}