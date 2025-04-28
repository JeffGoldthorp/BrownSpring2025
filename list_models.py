from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

# 🧠 TEMP: Print to confirm your API key actually loaded
print("Loaded API key:", os.getenv("OPENAI_API_KEY"))

client = OpenAI()

# List available models
models = client.models.list()

print("✅ Connected to OpenAI, printing models:")

for model in models.data:
    print(model.id)

