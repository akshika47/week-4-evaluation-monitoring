"""
Frontend Deployment Example - Streamlit
Deploy this to Streamlit Cloud
"""

import streamlit as st
import requests

st.title("🔍 AI Research Assistant")

# Get API URL from secrets (set in Streamlit Cloud)
API_URL = st.secrets.get("API_URL", "http://localhost:8000")

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if query := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)
    
    # Get response from API
    with st.chat_message("assistant"):
        with st.spinner("Researching..."):
            try:
                res = requests.post(
                    f"{API_URL}/chat",
                    json={"message": query},
                    timeout=30
                )
                res.raise_for_status()
                response = res.json()["response"]
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except requests.exceptions.RequestException as e:
                error_msg = f"Error: Could not connect to API. {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

