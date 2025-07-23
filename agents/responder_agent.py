import os
from dotenv import load_dotenv
import google.generativeai as genai
from core.prompts import build_prompt

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response(query: str, docs: list[str]) -> str:
    prompt = build_prompt(query, docs)
    response = model.generate_content(prompt)
    return response.text
