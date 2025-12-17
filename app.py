import streamlit as st
import pandas as pd
from model import generate_final_response

def set_green_theme():
    st.markdown(
        """
        <style>
        /* Main background */
        .stApp {
            background-color: #f0fdf4;
            color: #064e3b;
        }

        /* Headings */
        h1, h2, h3, h4 {
            color: #166534;
        }

        /* Normal text */
        p, span, label {
            color: #064e3b;
        }

        /* Input box */
        input, textarea {
            background-color: #ecfdf5 !important;
            color: #064e3b !important;
            border: 1px solid #22c55e !important;
            border-radius: 6px;
        }

        /* Buttons */
        .stButton > button {
            background-color: #22c55e;
            color: #064e3b;
            border-radius: 8px;
            font-weight: 600;
        }

        .stButton > button:hover {
            background-color: #16a34a;
            color: white;
        }

        /* Selectbox */
        div[data-baseweb="select"] > div {
            background-color: #ecfdf5;
            color: #064e3b;
            border: 1px solid #22c55e;
        }

        /* Spinner */
        .stSpinner > div {
            color: #166534;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

   
st.set_page_config(page_title="KanoonMitra - कानूनी मार्गदर्शक ", layout="wide")
set_green_theme()
st.title("⚖️ KanoonMitra: Your Indian Legal Assistant")
st.markdown("Enter your grievance or query in plain English (e.g., *'Theft of my mobile phone'*):")

user_query = st.text_input("📝 Type your issue below")

if st.button("🔍 Analyze"):
    with st.spinner("Analyzing relevant BNS sections..."):
        result = generate_final_response(user_query)
        st.session_state.result = result

# Display the result only if available
if "result" in st.session_state:
    result = st.session_state.result
    st.markdown("## 🧠 Summary ")
    st.markdown(result["summary"])

    # 3. Ask what user wants next
    st.subheader("🔍 What would you like to explore next?")
    option = st.selectbox(
        "Choose one:",
        (
            "📌 Mapped IPC Sections",
            "📘 BNS Section Descriptions",
            "🧑‍⚖️ Legal Advice",
            "📂 Case History (Links)"
        )
    )

    if st.button("Show Selected Section"):
        if option == "📌 Mapped IPC Sections":
            st.markdown("### 📌 Mapped IPC Sections")
            st.text(result["ipc_mapping"])

        elif option == "📘 BNS Section Descriptions":
            st.markdown("### 📘 BNS Section Descriptions")
            st.markdown(result["bns_descriptions"])

        elif option == "🧑‍⚖️ Legal Advice":
            st.markdown("### 🧑‍⚖️ Legal Advice")
            st.markdown(result["advice"])

        elif option == "📂 Case History (Links)":
            st.markdown("### 📂 Case History (Links)")
            st.markdown(result["case_links"])
