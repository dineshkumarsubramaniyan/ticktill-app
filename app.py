import html

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


def render_chat_thread_html(thread):
    parts = ['<div class="chat-shell">']
    if not thread:
        parts.append('<div class="chat-empty">Send a message to the bot and it will appear here.</div>')
    for item in thread:
        direction = item.get("direction", "owner_to_visitor")
        bubble_class = "chat-row left" if direction == "owner_to_visitor" else "chat-row right"
        bubble_kind = "chat-bubble owner" if direction == "owner_to_visitor" else "chat-bubble visitor"
        text = html.escape(item.get("text", ""))
        created_at = item.get("created_at", "")
        time_text = html.escape(created_at[11:16]) if len(created_at) >= 16 else ""
        parts.append(
            f'<div class="{bubble_class}">'
            f'<div class="{bubble_kind}">'
            f'<div class="chat-text">{text}</div>'
            f'<div class="chat-time">{time_text}</div>'
            f'</div></div>'
        )
    parts.append('</div>')
    return ''.join(parts)


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
.chat-shell {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 4px 0 10px;
}
.chat-empty {
  padding: 14px 16px;
  border-radius: 18px;
  background: #f7f2ee;
  color: #8b7b73;
  text-align: center;
  font-size: 0.95rem;
}
.chat-row {
  display: flex;
  width: 100%;
}
.chat-row.left {
  justify-content: flex-start;
}
.chat-row.right {
  justify-content: flex-end;
}
.chat-bubble {
  max-width: min(78%, 460px);
  padding: 10px 12px 8px;
  border-radius: 18px;
  box-shadow: 0 8px 18px rgba(90, 66, 58, 0.06);
}
.chat-bubble.owner {
  background: #f6eee9;
  color: #342521;
  border-top-left-radius: 6px;
}
.chat-bubble.visitor {
  background: #ead7ce;
  color: #2f211d;
  border-top-right-radius: 6px;
}
.chat-text {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.4;
  font-size: 0.98rem;
}
.chat-time {
  margin-top: 6px;
  font-size: 0.72rem;
  color: #8a776f;
  text-align: right;
}
div[data-testid="stTextArea"] textarea {
  border-radius: 16px;
  min-height: 96px;
}
div[data-testid="stForm"] {
  border: 0;
  padding: 0;
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
st.caption("Your Telegram messages appear on the left. Replies from the app go back to Telegram and stay on the right.")

chat_container = st.container()

@st.fragment(run_every="4s")
def render_chat_messages():
    thread = get_chat_thread(visitor_name)
    chat_container.markdown(render_chat_thread_html(thread), unsafe_allow_html=True)

render_chat_messages()

with st.form("reply_form", clear_on_submit=True):
    reply = st.text_area("Type a reply", key="visitor_reply_box", label_visibility="collapsed", placeholder=f"Reply as {visitor_name}...")
    submitted = st.form_submit_button("Send")
    if submitted:
        if send_visitor_reply(visitor_name, reply):
            st.rerun()
        else:
            st.error("Could not send the reply to Telegram. Check your app secrets and bot setup.")