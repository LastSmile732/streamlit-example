from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import requests
"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


# Run this with: streamlit run streamlit_app.py
# Streamlit interface
st.title("Gemini Central Console Bot")
user_input = st.text_input("Enter your text here")
url = "https://f1c8-34-142-152-37.ngrok-free.app/predict"  # URL of your FastAPI predict endpoint

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
