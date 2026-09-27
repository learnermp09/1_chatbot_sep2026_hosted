import streamlit as st
import requests

API_URL = "https://one-chatbot-sep2026-hosted.onrender.com/chat"

st.title("✨LLM AI Chatbot")

input_text = st.text_input("Enter your question here")

if input_text:
    response = requests.post(API_URL, json={"message": input_text})
    if response.status_code == 200:
        answer = response.json().get("response", "No response key found")
    else:
        answer = f"{response.status_code} : {response.text}"
    st.write(answer)