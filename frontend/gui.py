import streamlit as st
import requests

st.title("Customer Support AI Chatbot")
if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Enter your question:")
if st.button("Send"):
    response = requests.post("http://localhost:8000/query", json={"query": query})
    summary = response.json().get("summary", "")
    st.session_state.history.append((query, summary))

for q, a in st.session_state.history:
    st.write(f"**User:** {q}")
    st.write(f"**Bot:** {a}")
