import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="Wedding Countdown", layout="centered")

# Hide Streamlit UI
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Main container
container = st.empty()

def get_event():
    now = datetime.now()
    event = datetime(now.year, 9, 13, 0, 0, 0)
    if now > event:
        event = datetime(now.year + 1, 9, 13, 0, 0, 0)
    return event

event = get_event()

while True:
    now = datetime.now()
    diff = event - now

    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    seconds = diff.seconds % 60

    container.markdown(f"""
    <style>
    .card {{
        display: flex;
        max-width: 800px;
        margin: auto;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0px 10px 40px rgba(0,0,0,0.3);
        font-family: 'Georgia', serif;
    }}

    .left {{
        width: 50%;
        background: url('https://images.unsplash.com/photo-1522673607200-164d1b6ce486?q=80') center/cover no-repeat;
        min-height: 400px;
    }}

    .right {{
        width: 50%;
        background: #f7f7f7;
        padding: 40px;
        text-align: center;
    }}

    .title {{
        font-size: 28px;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }}

    .subtitle {{
        font-size: 14px;
        color: gray;
        margin-bottom: 30px;
    }}

    .timer {{
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
    }}

    .time-box {{
        text-align: center;
    }}

    .number {{
        font-size: 32px;
        font-weight: bold;
    }}

    .label {{
        font-size: 12px;
        color: gray;
        letter-spacing: 1px;
    }}
    </style>

    <div class="card">
        <div class="left"></div>

        <div class="right">
            <div class="title">WE'RE GETTING MARRIED</div>
            <div class="subtitle">COUNTDOWN TO OUR BIG DAY</div>

            <div class="timer">
                <div class="time-box">
                    <div class="number">{days:02}</div>
                    <div class="label">DAYS</div>
                </div>
                <div class="time-box">
                    <div class="number">{hours:02}</div>
                    <div class="label">HOURS</div>
                </div>
                <div class="time-box">
                    <div class="number">{minutes:02}</div>
                    <div class="label">MINUTES</div>
                </div>
                <div class="time-box">
                    <div class="number">{seconds:02}</div>
                    <div class="label">SECONDS</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(1)
