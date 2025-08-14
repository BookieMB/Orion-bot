# test_llm.py
from app.llm import call_llm

prompt = "Hello from the Gemini API via FastAPI!"
print("Sending prompt:", prompt)
reply = call_llm(prompt)
print("Model reply:", reply)
