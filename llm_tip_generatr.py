import streamlit as st
from llm_tip_generator import generate_llm_tip
import random

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Accessibility Simulation View",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HEADER ---
st.title("🔍 Simulation View")
st.markdown("Experience how a website appears to different users with accessibility needs.")

# --- SELECTED PERSONA ---
selected_persona = st.selectbox("👤 Selected Persona", [
    "Low Literacy",
    "Cognitive Overload",
    "Visual Impairment"
])

# --- SLIDER FOR INTENSITY ---
simulation_level = st.slider(
    "Adjust Simulation Intensity",
    min_value=1,
    max_value=5,
    value=3,
    help="Increase or decrease the severity of accessibility barriers."
)

# --- WEBSITE PREVIEW SIMULATION ---
st.subheader("🖥️ Website Preview")
placeholder = st.empty()

if selected_persona == "Low Literacy":
    placeholder.markdown(
        f"<div style='background-color:#fefae0; padding:20px; font-size:{16 + simulation_level}px;'>"
        "<strong>Example Header</strong><br>"
        "Some content might be difficult to understand due to complex wording and structure." 
        "<br><em>Important terms might be misunderstood or ignored.</em>"
        "</div>", unsafe_allow_html=True
    )
elif selected_persona == "Cognitive Overload":
    placeholder.markdown(
        f"<div style='background-color:#ffcccc; padding:20px; font-size:{12 + simulation_level}px;'>"
        "<strong>Too much info at once!</strong><br>"
        "Simulated layout shows distraction and clutter. Navigation feels overwhelming."
        "</div>", unsafe_allow_html=True
    )
else:
    placeholder.markdown(
        f"<div style='background-color:#d9edf7; padding:20px; font-size:{14 + simulation_level}px;'>"
        "<strong>Low Contrast Simulation</strong><br>"
        "Some text is hard to read. Buttons are faint. Important icons may not be distinguishable."
        "</div>", unsafe_allow_html=True
    )

# --- TOOLTIP CHECKLIST ---
st.markdown("---")
st.subheader("✅ Accessibility Issue Checklist")
st.markdown("Hover over each item to see why it matters.")

issues = [
    "Content too complex",
    "Too many elements",
    "Low contrast text",
    "No image alt text",
    "Unclear navigation"
]

for issue in issues:
    st.checkbox(f"{issue}", help=generate_llm_tip(issue))

# --- DOWNLOAD REPORT ---
st.markdown("---")
st.subheader("📄 Export Report")
st.download_button(
    label="Download Simulation Summary (PDF)",
    data="Placeholder PDF content for export",  # Replace with actual file content generation
    file_name="accessibility_simulation_report.pdf",
    mime="application/pdf"
)

# --- FEEDBACK NOTE ---
st.markdown("""
*This simulation is educational and does not store user data.*
""")
