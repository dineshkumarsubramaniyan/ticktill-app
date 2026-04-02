import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

# ✅ MUST be first
st.set_page_config(
    page_title="TickTill 💍",
    page_icon="💍",
    layout="centered"
)

# ✅ Hide Streamlit UI
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ✅ PWA + Mobile Install Config (VERY IMPORTANT)
st.markdown("""
<link rel="manifest" href="data:application/manifest+json,{
    \\"name\\": \\"TickTill 💍\\",
    \\"short_name\\": \\"TickTill\\",
    \\"start_url\\": \\"/\\",
    \\"display\\": \\"standalone\\",
    \\"background_color\\": \\"#f4f4f4\\",
    \\"theme_color\\": \\"#f4f4f4\\",
    \\"icons\\": [
        {
            \\"src\\": \\"https://cdn-icons-png.flaticon.com/512/833/833472.png\\",
            \\"sizes\\": \\"512x512\\",
            \\"type\\": \\"image/png\\"
        }
    ]
}">
<link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/833/833472.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="TickTill">
""", unsafe_allow_html=True)

# ✅ Event date logic
def get_event():
    now = datetime.now()
    event = datetime(now.year, 9, 13, 0, 0, 0)
    if now > event:
        event = datetime(now.year + 1, 9, 13, 0, 0, 0)
    return event

event = get_event()

# ✅ Beautiful Responsive UI + JS countdown
components.html(f"""
<!DOCTYPE html>
<html>
<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
body {{
    margin: 0;
    padding: 10px;
    background: #f4f4f4;
    font-family: 'Georgia', serif;
}}

.container {{
    max-width: 420px;
    margin: auto;
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.15);
}}

/* IMAGE */
.image {{
    width: 100%;
    height: 220px;
    background: url('https://images.unsplash.com/photo-1522673607200-164d1b6ce486?q=80') center/cover no-repeat;
}}

/* CONTENT */
.content {{
    padding: 25px 20px;
    text-align: center;
}}

.title {{
    font-size: 20px;
    letter-spacing: 2px;
    margin-bottom: 5px;
}}

.subtitle {{
    font-size: 12px;
    color: #777;
    margin-bottom: 20px;
}}

/* TIMER GRID */
.timer {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
}}

.box {{
    background: #fafafa;
    padding: 15px;
    border-radius: 12px;
}}

.number {{
    font-size: 28px;
    font-weight: bold;
}}

.label {{
    font-size: 10px;
    color: #888;
    letter-spacing: 1px;
}}
</style>

</head>

<body>

<div class="container">
    <div class="image"></div>

    <div class="content">
        <div class="title">WE'RE GETTING MARRIED</div>
        <div class="subtitle">COUNTDOWN TO OUR BIG DAY</div>

        <div class="timer">
            <div class="box"><div id="days" class="number"></div><div class="label">DAYS</div></div>
            <div class="box"><div id="hours" class="number"></div><div class="label">HOURS</div></div>
            <div class="box"><div id="minutes" class="number"></div><div class="label">MINUTES</div></div>
            <div class="box"><div id="seconds" class="number"></div><div class="label">SECONDS</div></div>
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
""", height=620)