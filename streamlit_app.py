# app.py
import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import google.generativeai as genai

# 1. Configure Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("Missing GEMINI_API_KEY in environment variables")
    st.stop()
genai.configure(api_key=API_KEY)

# 2. UI layout
st.set_page_config(page_title="My Gemini-Streamlit App", layout="centered")
st.title("AI Chat with Gemini via Streamlit")
st.write("Ask me anything:")

if "history" not in st.session_state:
    st.session_state.history = []

# 3. Handle user input
user_input = st.text_input("You:", key="input")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    # Show user message
    with st.chat_message("user"):
        st.write(user_input)
    # Call Gemini model
    with st.chat_message("assistant"):
        st.write("Thinking...")
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")  # or whatever model name
            response = model.generate_content(user_input)
            answer = response.text
        except Exception as e:
            answer = f"Error: {e}"
        st.write(answer)
    st.session_state.history.append({"role": "assistant", "content": answer})
    # clear input box for next message
    st.experimental_rerun()

# 4. Display history (optional)
for msg in st.session_state.history:
    author = "You" if msg["role"]=="user" else "Assistant"
    st.write(f"**{author}:** {msg['content']}")
