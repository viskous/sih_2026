from fastapi import FastAPI
from pydantic import BaseModel
from recommender.recommend import recommend
from dialogue.extract_profile import extract_profile

app = FastAPI()

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
    return {"extracted_profile": profile, "recommendations": results}