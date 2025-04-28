from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import time
import os

# Load API key
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

client = OpenAI()

# Directory containing your JSONL files
JSONL_DIR = Path(__file__).parent / "jsonl-files"

# Upload valid JSONL files
file_ids = []
for file_name in os.listdir(JSONL_DIR):
    if file_name.endswith(".jsonl"):
        file_path = JSONL_DIR / file_name
        with open(file_path, "rb") as f:
            response = client.files.create(file=f, purpose="fine-tune")
            file_ids.append(response.id)
            print(f"Uploaded {file_name} → File ID: {response.id}")

# Fine-tune model (use the first uploaded file)
if file_ids:
    response = client.fine_tuning.jobs.create(
        training_file=file_ids[0],
        model="gpt-3.5-turbo-1106",  # you are fine-tuning on GPT-3.5-turbo
        hyperparameters={
            "n_epochs": 3,
            "batch_size": "auto",
            "learning_rate_multiplier": "auto"
        }
    )
    job_id = response.id
    print(f"🚀 Fine-tuning job created: {job_id}")

    # Track fine-tuning progress
    while True:
        job_status = client.fine_tuning.jobs.retrieve(job_id)
        print(f"Status: {job_status.status}")

        if job_status.status in ["succeeded", "failed"]:
            print(f"✅ Final status: {job_status.status}")
            if job_status.status == "succeeded":
                print(f"🎯 Fine-tuned model ID: {job_status.fine_tuned_model}")
            break

        time.sleep(60)  # Check every 60 seconds

else:
    print("❌ No valid JSONL files uploaded.")
