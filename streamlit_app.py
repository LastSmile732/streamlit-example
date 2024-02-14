from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import requests

df_hourly_m = pd.read_csv('./UsagePerHourMerged.csv', delimiter=',')
df_hourly_m['Date'] = pd.to_datetime(df_hourly_m['Date'])


# Run this with: streamlit run streamlit_app.py
# Streamlit interface
st.title("Gemini Central Console Bot")
action = st.selectbox("Choose an action:", ["draw_line_chart", "generate_answer"])

if action == "draw_line_chart":
    # UI for line chart request
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    # Filter DataFrame based on date range
    mask = (df_hourly_m['Date'] >= pd.Timestamp(start_date)) & (df_hourly_m['Date'] <= pd.Timestamp(end_date))
    filtered_df = df_hourly_m.loc[mask]
        
    # Plotting
    # Ensure that 'Date' is the index if you want it on the x-axis
    st.line_chart(filtered_df.set_index('Date')['TotalMeterUsage'])
        
elif action == "generate_answer":
    user_input = st.text_area("Enter your text here")
    url = "https://69a2-34-143-149-55.ngrok-free.app/v1/completions"  # URL of your FastAPI predict endpoint

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
            st.write(response.text)



        
