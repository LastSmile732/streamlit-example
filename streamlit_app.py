from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import requests
from datetime import datetime

df_hourly_m = pd.read_csv('./UsagePerHourMerged.csv', delimiter=',')
df_hourly_m['Date'] = pd.to_datetime(df_hourly_m['Date'])


# Run this with: streamlit run streamlit_app.py
# Streamlit interface
st.title("Gemini Central Console Bot")
action = st.selectbox("Choose an action:", ["draw_line_chart", "generate_answer"])
host = "https://af05-34-87-50-186.ngrok-free.app"

if action == "draw_line_chart":
    url = host + "/analyse"
    # UI for line chart request
    st.write("Select the Merchant Device ID:")
    unique_device_ids = df_hourly_m['MerchantDevice_id'].unique()
    selected_device_id = st.selectbox('MerchantDevice_id', unique_device_ids)

    st.write("Select the date range:")
    start_date = st.date_input("Start Date", value=pd.to_datetime(datetime.today().strftime('%Y-%m-%d')))
    end_date = st.date_input("End Date", value=pd.to_datetime(datetime.today().strftime('%Y-%m-%d')))

    if st.button("Draw"):
        # Convert 'Date' column to datetime if it's not already
        df_hourly_m['Date'] = pd.to_datetime(df_hourly_m['Date'])
        
        # Filter DataFrame based on selected MerchantDevice_id and date range
        mask = ((df_hourly_m['Date'] >= pd.Timestamp(start_date)) & 
                (df_hourly_m['Date'] <= pd.Timestamp(end_date)) & 
                (df_hourly_m['MerchantDevice_id'] == selected_device_id))
        filtered_df = df_hourly_m.loc[mask]
        
        if not filtered_df.empty:
            total_usage_series = filtered_df['TotalUsage'].tolist()
            series_text = ', '.join([f"{value:.2f}" for value in total_usage_series])
            payload = {"data": series_text}
            st.write("Drawing the line chart....")
            
            # Plotting
            st.line_chart(filtered_df.set_index('Date')['TotalUsage'])

            # Send the request to FastAPI endpoint
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                st.write(content)
            else:
                st.error("Failed to get a response from the server.")
                st.write(response.text)
        else:
            st.error("No data available for the selected device ID and date range.")
        
elif action == "generate_answer":
    user_input = st.text_area("Enter your text here")
    url = host + "/dataframe"  # URL of your FastAPI predict endpoint

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



        
