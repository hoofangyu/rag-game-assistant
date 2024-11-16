import streamlit as st
import requests
import uuid

ip = "34.207.66.130"

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

st.title("Game Query Assistant")
st.write("Ask questions about games, and get answers based on the games dataset.")

query_text = st.text_input("Enter your question about games:")

if st.button("Get Answer"):
    if query_text:
        try:
            url = f"http://{ip}:5000/answer_query"
            payload = {"query": query_text, "session_id": st.session_state["session_id"]}
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                result = response.json().get("result")
                history = response.json().get("chat_memory")
                st.write("Answer:", result)
                st.write("History:", history)
            else:
                st.error(f'"Error from Flask API:", {response.text}')
        except Exception as e:
            st.error(f"Error connecting to the API: {e}")
    else:
        st.warning("Please enter a query to proceed.")
