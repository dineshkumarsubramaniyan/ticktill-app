import streamlit as st
import streamlit.components.v1 as components

from ui.css import get_css
from ui.html import get_html
from ui.js import get_js
from utils.date_utils import get_event_date

# Config
st.set_page_config(
    page_title="TickTill 💍",
    page_icon="💍",
    layout="centered"
)

# Hide Streamlit UI
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Get event date
event = get_event_date()
event_str = event.strftime('%Y-%m-%d %H:%M:%S')

# Combine all parts
full_code = f"""
<style>{get_css()}</style>
{get_html()}
{get_js(event_str)}
"""

# Render
components.html(full_code, height=650)