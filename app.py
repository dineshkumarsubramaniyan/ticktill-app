import streamlit as st
import streamlit.components.v1 as components

from ui.css import get_css
from ui.html import get_html
from ui.js import get_js
from ui.media import get_audio_source
from utils.date_utils import get_event_date
from utils.visitor_notifications import (
    get_chat_thread,
    get_visitor_name,
    send_visitor_reply,
    track_visitor_open,
)

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
[data-testid="stChatMessage"] {
  border-radius: 18px;
}
[data-testid="stChatInput"] {
  position: sticky;
  bottom: 0;
}
</style>
""", unsafe_allow_html=True)

visitor_name = get_visitor_name(st.query_params)
if not st.session_state.get("visitor_tracked"):
    track_visitor_open(visitor_name)
    st.session_state["visitor_tracked"] = True

event = get_event_date()
event_str = event.strftime('%Y-%m-%d %H:%M:%S')
audio_src, audio_available = get_audio_source()

full_code = f"""
<style>{get_css()}</style>
{get_html(audio_src, audio_available)}
{get_js(event_str, audio_available, "")}
"""

components.html(full_code, height=820, scrolling=False)

st.markdown("### Private Chat")
st.caption("Messages you send to the bot appear here. Replies typed here will be sent back to Telegram.")

thread = get_chat_thread(visitor_name)
for item in thread:
    if item.get("direction") == "owner_to_visitor":
        with st.chat_message("assistant"):
            st.write(item.get("text", ""))
    else:
        with st.chat_message("user"):
            st.write(item.get("text", ""))

reply = st.chat_input(f"Reply as {visitor_name}...")
if reply:
    if send_visitor_reply(visitor_name, reply):
        st.rerun()
    else:
        st.error("Could not send the reply to Telegram. Check your app secrets and bot setup.")