import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

# Sidebar CSS customization
st.markdown("""
    <style>
    /* Customize sidebar */
    .css-1lcbmhc {  /* Streamlit's sidebar class */
        background-color: #1E1E1E; /* Dark gray-black background */
        border-radius: 10px; /* Rounded corners */
        color: #EAEAEA; /* Light gray text */
        padding: 20px; /* Add padding */
        margin: 20px 0; /* Space around the sidebar */
    }

    /* Select box customization */
    .stSelectbox > div {
        font-size: 16px;
        font-weight: bold;
        font-family: 'Arial', sans-serif; /* Clean, modern font */
        background-color: #2A2A2A; /* Medium gray background */
        border: 1px solid #4A4A4A; /* Subtle border */
        color: #F5F5F5; /* Almost white text */
        border-radius: 8px; /* Rounded corners */
        text-align: center;
        padding: 5px;
        transition: 0.3s ease-in-out;
    }

    /* Select box hover effect */
    .stSelectbox > div:hover {
        background-color: #3A3A3A; /* Slightly lighter gray */
        border-color: #5A5A5A; /* Matte border */
        transform: scale(1.02); /* Subtle zoom on hover */
    }

    /* Sidebar text styling */
    .stSidebar div {
        font-size: 14px;
        font-family: 'Arial', sans-serif;
        color: #C8C8C8; /* Light gray text */
    }

    /* Adjust margin and padding for cleaner layout */
    .css-1aumxhk {
        padding: 10px 20px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation
page = st.sidebar.selectbox("Explore Or Predict", ("Predict", "Explore"))

# Page selection logic
if page == "Predict":
    show_predict_page()
else:
    show_explore_page()
