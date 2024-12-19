import streamlit as st
import pandas as pd
import requests

# API endpoints
BACKEND_URL = "http://127.0.0.1:8000"

# Load data from backend
st.title("Smart Incident Management System (SIMS)")
st.sidebar.title("Filters")

# Fetch data from backend
@st.cache_data
def fetch_data():
    response = requests.get(f"{BACKEND_URL}/incidents")
    return pd.DataFrame(response.json())

data = fetch_data()
st.dataframe(data)

# Filter by severity
severity_filter = st.sidebar.multiselect("Filter by Severity", options=data["severity"].unique())
if severity_filter:
    filtered_data = data[data["severity"].isin(severity_filter)]
    st.dataframe(filtered_data)

# Add AI Classification
st.header("Classify New Incident")
description = st.text_area("Enter Incident Description:")
if st.button("Classify"):
    response = requests.post(f"{BACKEND_URL}/classify", json={"description": description})
    result = response.json()
    st.write(f"**Category:** {result['category']} (Confidence: {result['confidence']:.2f})")

# Display summary
st.header("Incident Summary")
response = requests.get(f"{BACKEND_URL}/summary")
summary = pd.DataFrame(response.json())
st.bar_chart(summary.set_index("severity"))
