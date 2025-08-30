
import requests
import streamlit as st
import os


BACKEND_URL = os.getenv("BACKEND_URL")


st.set_page_config(page_title="Intelligent IT Support Assistant", page_icon="🤖")




st.title("Intelligent IT Support Agent")


if "history" not in st.session_state:
    st.session_state.history = [] # list of dicts: {role, content}


for msg in st.session_state.history:
    if msg["role"] in ["tool-call", "tool-call-output","system"]:
        continue  # Skip displaying these messages
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_input = st.chat_input("Ask me anything…")


if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)


    # Call backend
    payload = {
    "messages": st.session_state.history,
    }
    try:
        r = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=180)
        r.raise_for_status()
        data = r.json()
        reply = data.get("reply", "(no reply)")
        new_messages = data.get("messages", [])
    except Exception as e:
        reply = f"Error: {e}"
        new_messages = []

    # Only append new messages that are not already in the session history
    existing = len(st.session_state.history)
    for msg in new_messages[existing:]:
        st.session_state.history.append(msg)
        if msg["role"] in ["tool-call", "tool-call-output", "system"]:
            continue  # Skip displaying these messages
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])