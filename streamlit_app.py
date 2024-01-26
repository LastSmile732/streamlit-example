from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import requests

# Run this with: streamlit run streamlit_app.py
# Streamlit interface
st.title("Gemini Central Console Bot")
user_input = st.text_input("Enter your text here")
url = "https://5f8b-34-126-161-223.ngrok-free.app/predict"  # URL of your FastAPI predict endpoint

if st.button("Submit"):
    # Prepare the payload
    payload = {"prompt": user_input}

    # Send the request to FastAPI endpoint
    response = requests.post(url, json=payload)

    # Display the response
    if response.status_code == 200:
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        st.write(content)
    else:
        st.write("Failed to get response")
