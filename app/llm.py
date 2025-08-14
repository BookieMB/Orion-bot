# app/llm.py
import google.generativeai as genai
import os

# Load your Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY environment variable.")

# Configure Gemini client
genai.configure(api_key=GEMINI_API_KEY)

# Model to use
GEMINI_MODEL = "gemini-1.5-flash"

def call_llm(prompt: str) -> str:
    """Call Gemini and return its reply."""
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    return response.text