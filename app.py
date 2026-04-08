import streamlit as st
import streamlit.components.v1 as components

from ui.css import get_css
from ui.html import get_html
from ui.js import get_js
from ui.media import get_audio_source
from utils.date_utils import get_event_date
from utils.visitor_notifications import get_popup_message, get_visitor_name, track_visitor_open

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

visitor_name = get_visitor_name(st.query_params)
if not st.session_state.get("visitor_tracked"):
    track_visitor_open(visitor_name)
    st.session_state["visitor_tracked"] = True

popup_message = get_popup_message()
event = get_event_date()
event_str = event.strftime('%Y-%m-%d %H:%M:%S')
audio_src, audio_available = get_audio_source()

full_code = f"""
<style>{get_css()}</style>
{get_html(audio_src, audio_available)}
{get_js(event_str, audio_available, popup_message)}
"""

components.html(full_code, height=820, scrolling=False)