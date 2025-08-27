
import requests
import streamlit as st
import os


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


st.set_page_config(page_title="HF Chatbot", page_icon="🤖")


with st.sidebar:
    st.title("⚙️ Settings")
    model = st.text_input("Model", value="openai/gpt-oss-20b")
    max_new_tokens = st.slider("Max new tokens", 16, 1024, 256, 8)
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    top_p = st.slider("Top-p", 0.0, 1.0, 0.95, 0.05)
    st.markdown("""
    **Tip:** Try other instruction-tuned models like:
    - `mistralai/Mistral-Nemo-Instruct-2407`
    - `meta-llama/Llama-3.1-8B-Instruct`
    """)


st.title("🤖 HF Inference API Chatbot")


if "history" not in st.session_state:
    st.session_state.history = [] # list of dicts: {role, content}


for msg in st.session_state.history:
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
    "model": model,
    "max_new_tokens": max_new_tokens,
    "temperature": temperature,
    "top_p": top_p,
    }
    try:
        r = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=180)
        r.raise_for_status()
        data = r.json()
        reply = data.get("reply", "(no reply)")
    except Exception as e:
        reply = f"Error: {e}"


    st.session_state.history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)