# pages/2_Accessibility_Chatbot.py

import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Accessibility Chatbot", layout="centered")
st.title("💬 Accessibility Chatbot")
st.markdown("Ask anything about digital accessibility, WCAG rules, or inclusive design!")

# Initialize chat history
if "access_chat_history" not in st.session_state:
    st.session_state.access_chat_history = [
        {"role": "system", "content": "You are an expert in digital accessibility. You help users understand WCAG rules, inclusive design principles, and practical tips to improve accessibility for people with disabilities. Keep your tone friendly and explain clearly with examples when possible."}
    ]

# User input
user_question = st.text_input("Type your accessibility question here:", key="access_chat_input")

if st.button("Send", key="access_chat_send"):
    if user_question:
        st.session_state.access_chat_history.append({"role": "user", "content": user_question})

        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.access_chat_history
        )

        reply = response.choices[0].message.content
        st.session_state.access_chat_history.append({"role": "assistant", "content": reply})

        st.markdown("### 🤖 AI Assistant")
        st.write(reply)
    else:
        st.warning("Please enter a question first.")

# Optional: Show chat history (if you want to display the full thread)
with st.expander("🕘 Chat History"):
    for msg in st.session_state.access_chat_history[1:]:  # skip system prompt
        role = "👤 You" if msg["role"] == "user" else "🤖 AI"
        st.markdown(f"**{role}:** {msg['content']}")
