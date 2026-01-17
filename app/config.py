import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = os.getenv("HF_MODEL")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("HF_API_KEY loaded:", "✅" if HF_API_KEY else "❌")
print("HF_MODEL loaded:", HF_MODEL)
print("GEMINI_API_KEY loaded:", "✅" if GEMINI_API_KEY else "❌")
print("GEMINI_MODEL loaded:", GEMINI_MODEL)
