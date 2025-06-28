import streamlit as st
from openai import OpenAI

# Initialize OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Define WCAG rules and personas
personas = [
    "low literacy",
    "cognitive load challenges",
    "visual impairment",
    "motor impairment",
    "older adults with declining digital skills",
    "non-native language speakers"
]

wcag_rules = [
    {"id": "1.1.1", "title": "Non-text Content", "description": "Provide text alternatives for any non-text content.", "personas": "visual impairment, cognitive load challenges"},
    {"id": "1.2.1", "title": "Audio-only and Video-only", "description": "Provide alternatives for audio-only and video-only content.", "personas": "visual impairment, older adults with declining digital skills"},
    {"id": "1.2.2", "title": "Captions (Prerecorded)", "description": "Provide captions for prerecorded audio.", "personas": "non-native language speakers, hearing impairment"},
    {"id": "1.3.1", "title": "Info and Relationships", "description": "Ensure information and relationships can be determined programmatically.", "personas": "low literacy, cognitive load challenges"},
    {"id": "1.3.2", "title": "Meaningful Sequence", "description": "Content must be in a meaningful order.", "personas": "cognitive load challenges, older adults with declining digital skills"},
    # ... (Add the rest of your rules as needed)
]

def generate_why_this_matters(rule_title, rule_description, persona):
    prompt = f"""
Accessibility Rule: {rule_title}
Description: {rule_description}

This issue affects {persona}. Please explain why this accessibility issue matters for them in plain language.
Use a helpful, gentle tone. Keep the explanation short, and use a maximum of 3 sentences.
Avoid jargon, and speak as if guiding a non-technical healthcare staff member using an accessibility simulation tool for the first time.
"""
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are an accessibility assistant helping explain accessibility barriers to non-technical healthcare professionals."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# --- Streamlit App Start ---
st.set_page_config(page_title="Accessibility Explainer", layout="centered")
st.title("🧠 Why This Matters")

# Read query parameters
query_params = st.query_params
selected_rule_title = query_params.get("rule", "")
selected_persona = query_params.get("persona", "")

# Show selected values
if selected_rule_title and selected_persona:
    st.markdown(f"**Persona:** {selected_persona}<br>**Issue:** {selected_rule_title}", unsafe_allow_html=True)

    selected_rule = next((rule for rule in wcag_rules if rule["title"] == selected_rule_title), None)
    if selected_rule:
        rule_description = selected_rule["description"]
        explanation = generate_why_this_matters(selected_rule_title, rule_description, selected_persona)
        st.write("### Why this Matters:")
        st.write(explanation)
    else:
        st.error("⚠️ WCAG rule not found. Please check the rule parameter in the URL.")
else:
    st.warning("Please provide both `persona` and `rule` in the URL query parameters.")

# --- Chat Assistant Section ---
st.markdown("---")
st.subheader("💬 Ask a Follow-up Question")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are an accessibility assistant for non-technical healthcare teams. Help explain WCAG rules clearly and give short, working code examples (e.g. HTML, CSS, ARIA, JS) to fix the problem. Be gentle and helpful."}
    ]

user_input = st.text_input("Type your question here:")

if st.button("Send") and user_input:
    # Add context if available
    context = ""
    if selected_rule_title:
        rule_description = next((rule["description"] for rule in wcag_rules if rule["title"] == selected_rule_title), "")
        context = f"""
The user is asking a follow-up question based on this WCAG rule:

Persona: {selected_persona}
Rule Title: {selected_rule_title}
Description: {rule_description}

Please include a small and simple code example (HTML/CSS/ARIA or JavaScript) that addresses this accessibility rule.
"""
    message = context + "\n\n" + user_input if context else user_input
    st.session_state.chat_history.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=st.session_state.chat_history
    )
    reply = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

    st.markdown("### 👩‍⚕️ Assistant's Answer")
    st.write(reply)
