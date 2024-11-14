import streamlit as st
import requests

# Streamlit app setup
st.title("Game Query Assistant")
st.write("Ask questions about games, and get answers based on the games dataset.")

# User input for query
query_text = st.text_input("Enter your question about games:")

# Submit button
if st.button("Get Answer"):
    # Send request to Flask API
    if query_text:
        try:
            # Flask API URL (assuming the Flask API is running on localhost:5000)
            url = "http://localhost:5000/answer_query"
            payload = {"query": query_text}
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                result = response.json().get("result")
                st.write("Answer:", result)
            else:
                st.error("Error from Flask API:", response.text)
        except Exception as e:
            st.error(f"Error connecting to the API: {e}")
    else:
        st.warning("Please enter a query to proceed.")
