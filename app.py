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
        font-size: 40px;
        font-weight: bold;
    }

    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='title'>📅 Event on Sept 13</div>", unsafe_allow_html=True)

# Placeholder for live countdown
countdown_placeholder = st.empty()

# Set event date
def get_event_date():
    now = datetime.now()
    event_date = datetime(now.year, 9, 13)

    if now > event_date:
        event_date = datetime(now.year + 1, 9, 13)

    return event_date

event = get_event_date()

# Live countdown loop
while True:
    now = datetime.now()
    diff = event - now

    days = diff.days
    seconds = diff.seconds

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    countdown_placeholder.markdown(
        f"<div class='count'>⏳ {days}d {hours}h {minutes}m {secs}s</div>",
        unsafe_allow_html=True
    )

    time.sleep(1)

st.markdown("</div>", unsafe_allow_html=True)
