import json
from dialogue.providers.gemini_provider import call_llm

SYSTEM_PROMPT = """You are extracting structured beneficiary information from a conversation for a livelihood-matching system.

Given the conversation text, output ONLY a JSON object with this exact structure, nothing else:

{
  "education_level": "string",
  "existing_skills": ["list", "of", "skills"],
  "interests": ["list", "of", "interests"],
  "employment_preference": "self" or "wage" or "both",
  "mobility_constraint": true or false,
  "region": "string"
}

If information for a field is missing, make a reasonable guess or use an empty string/list/false. Output ONLY the JSON, no explanation, no markdown formatting."""

def extract_profile(conversation_text):
    raw_text = call_llm(SYSTEM_PROMPT, conversation_text)
    raw_text = raw_text.strip("`").replace("json\n", "", 1).strip()
    profile = json.loads(raw_text)
    return profile