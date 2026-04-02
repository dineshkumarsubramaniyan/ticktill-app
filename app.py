import streamlit as st
from datetime import datetime
import time
import streamlit.components.v1 as components

# components.html(html_code, height=450)

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

components.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
.card {{
    display: flex;
    max-width: 800px;
    margin: auto;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0px 10px 40px rgba(0,0,0,0.3);
    font-family: Georgia, serif;
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

.number {{
    font-size: 32px;
    font-weight: bold;
}}

.label {{
    font-size: 12px;
    color: gray;
}}
</style>
</head>

<body>

<div class="card">
    <div class="left"></div>

    <div class="right">
        <h2>WE'RE GETTING MARRIED</h2>
        <p>COUNTDOWN TO OUR BIG DAY</p>

        <div style="display:flex; justify-content:space-around;">
            <div><div id="days" class="number"></div><div class="label">DAYS</div></div>
            <div><div id="hours" class="number"></div><div class="label">HOURS</div></div>
            <div><div id="minutes" class="number"></div><div class="label">MINUTES</div></div>
            <div><div id="seconds" class="number"></div><div class="label">SECONDS</div></div>
        </div>
    </div>
</div>

<script>
const eventDate = new Date("{event.strftime('%Y-%m-%d %H:%M:%S')}").getTime();

setInterval(function() {{
    const now = new Date().getTime();
    const diff = eventDate - now;

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((diff / (1000 * 60)) % 60);
    const seconds = Math.floor((diff / 1000) % 60);

    document.getElementById("days").innerHTML = days.toString().padStart(2,'0');
    document.getElementById("hours").innerHTML = hours.toString().padStart(2,'0');
    document.getElementById("minutes").innerHTML = minutes.toString().padStart(2,'0');
    document.getElementById("seconds").innerHTML = seconds.toString().padStart(2,'0');

}}, 1000);
</script>

</body>
</html>
""", height=450)

time.sleep(1)
