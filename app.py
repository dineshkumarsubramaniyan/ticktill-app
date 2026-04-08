import streamlit as st
import streamlit.components.v1 as components

from ui.css import get_css
from ui.html import get_html
from ui.js import get_js
from ui.media import get_audio_source
from utils.date_utils import get_event_date

st.set_page_config(
    page_title="TickTill",
    page_icon="*",
    layout="centered"
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

event = get_event_date()
event_str = event.strftime('%Y-%m-%d %H:%M:%S')
audio_src, audio_available = get_audio_source()

full_code = f"""
<style>{get_css()}</style>
{get_html(audio_src, audio_available)}
{get_js(event_str, audio_available)}
"""

components.html(full_code, height=820, scrolling=False)
