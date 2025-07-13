import streamlit as st
import os
from openai import OpenAI

# Windows-friendly setup
st.set_page_config(page_title="Windows Chatbot", page_icon="💻")

# Initialize chat (Windows needs explicit path handling)
if "messages" not in st.session_state:
    st.session_state.messages = []
    if os.name == 'nt':  # Windows-specific welcome
        st.session_state.messages.append({"role": "assistant", "content": "Hello from Windows! 🖥️"})

# Display chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input handling
if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Windows-friendly API handling
    try:
        client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", "sk-dummy"))  # Default dummy key for Windows
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            temperature=0.7
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"⚠️ Error (Windows users: check API key): {str(e)}"
    
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
