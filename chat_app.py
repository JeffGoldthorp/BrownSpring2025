import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Setup OpenAI client
client = OpenAI()

# Your fine-tuned model ID
FINE_TUNED_MODEL = "ftjob-7mrQ1tLqdYTqrCL9qm4QcvPe"  # replace if needed

# Streamlit page setup
st.set_page_config(page_title="Emergency Alerts Chatbot", page_icon="🚨")
st.title("🛰️ Telecom Cybersecurity Advisor")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an AI assistant specialized in emergency alerts, public safety communications, cybersecurity, disaster response, and FCC regulations."}
    ]

# Chat input
user_input = st.chat_input("Ask me about emergency alerts, public safety, or FCC regulations...")

if user_input:
    # Add user input to the session state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call the fine-tuned model
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model=FINE_TUNED_MODEL,
            messages=st.session_state.messages,
            temperature=0.2,
            max_tokens=300
        )
        assistant_reply = response.choices[0].message.content.strip()

    # Add assistant response to session
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

# Display conversation history
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])
