import streamlit as st
from why_this_matters_chatbot import generate_why_this_matters, wcag_rules

st.set_page_config(page_title="Persona Selection", layout="centered")

st.title("🧠 Accessibility Simulation Tool")
st.markdown("Choose a user persona to simulate how they experience your site:")

# Define persona cards
personas = {
    "Low Literacy - Age 65+": "May have difficulty with reading long or complex texts.",
    "Cognitive Load": "May find it hard to focus in a busy environment.",
    "Visual Impairment": "May struggle to read small text or see low-contrast elements.",
    "Autism Spectrum": "May become overwhelmed by animations or lack of consistency.",
    "Motor Impairment": "May struggle with small click targets due to limited mobility.",
    "Hearing Impairment": "May miss audio content or instructions without captions."
}

# Set default if not already selected
if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = list(personas.keys())[0]

# Display persona cards with radio buttons
selected = st.radio("Select Persona", list(personas.keys()), index=0, key="selected_persona", label_visibility="collapsed")

# Show cards
for label, description in personas.items():
    if selected == label:
        border = "3px solid #4B3DFE"
    else:
        border = "1px solid #ccc"
    
    with st.container():
        st.markdown(
            f"""
            <div style="border:{border}; border-radius:12px; padding:12px; margin:10px 0; background:#f9f9f9">
                <label>
                    <strong>{label}</strong><br>
                    <span style="color:#555">{description}</span>
                </label>
            </div>
            """,
            unsafe_allow_html=True
        )

# CTA Button
if st.button("👁️ See How This Persona Experiences the Web"):
    st.session_state.persona_ready = True
    st.success(f"Persona '{st.session_state.selected_persona}' selected.")
    
    # Example: run LLM explainer on a sample rule
    rule = next((r for r in wcag_rules if r["id"] == "1.4.3"), None)  # Contrast (Minimum)
    if rule:
        explanation = generate_why_this_matters(
            rule["title"],
            rule["description"],
            st.session_state.selected_persona
        )
        st.markdown("### 💬 Why this Matters for selected persona")
        st.write(explanation)
        # --- Chat with AI Assistant ---
        st.markdown("---")
        st.subheader("💬 Ask More Questions")
        
        # Keep track of chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                {"role": "system", "content": "You are an accessibility assistant for non-technical healthcare teams. Help explain WCAG rules clearly and give short, working code examples (e.g. HTML, CSS, ARIA, JS) to fix the problem. Be gentle and helpful."}
            ]
        
        # User input box
        user_input = st.text_input("Ask a follow-up question:", key="chat_input_box")
        
        # Send question
        if st.button("Send", key="chat_send_button"):
            if user_input:       
                if selected_rule_title and selected_rule_title != "":
                    rule_description = next((rule["description"] for rule in wcag_rules if rule["title"] == selected_rule_title), "")
                    context = f"""
                The user is asking a follow-up question based on this WCAG rule:
                
                Rule Title: {selected_rule_title}
                Description: {rule_description}
                
                Please include a small and simple code example (HTML/CSS/ARIA or JavaScript) that addresses this accessibility rule.
                """
                    st.session_state.chat_history.append({"role": "user", "content": context + "\n\n" + user_input})
                else:
                    st.session_state.chat_history.append({"role": "user", "content": user_input})
                # Get LLM response
                response = client.chat.completions.create(
                    model="gpt-4.1", 
                    messages=st.session_state.chat_history
                )
                reply = response.choices[0].message.content
        
                # Add assistant reply to history
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
        
                # Display chat
                st.markdown("### 👩‍⚕️ AI Assistant Response")
                st.write(reply)
            else:
                st.warning("Please type a question before clicking Send.")
