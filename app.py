import streamlit as st
from datetime import datetime
import time

st.set_page_config(
    page_title="TickTill",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit menu + footer
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .main {
        text-align: center;
    }

    .card {
        background: linear-gradient(135deg, #1e1e2f, #2c2c54);
        padding: 40px;
        border-radius: 20px;
        color: white;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
    }

    .title {
        font-size: 26px;
        margin-bottom: 20px;
    }

    .count {
        font-size: 50px;
        font-weight: bold;
    }

    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)

st.markdown("<div class='title'>📅 Event on Sept 13</div>", unsafe_allow_html=True)

today = datetime.now()
event = datetime(today.year, 9, 13)

if today > event:
    event = datetime(today.year + 1, 9, 13)

days = (event - today).days

st.markdown(f"<div class='count'>⏳ {days} days</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
