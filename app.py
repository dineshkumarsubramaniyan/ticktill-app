from urllib.parse import quote_plus
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


CHAT_HEIGHT = 620


def build_nav_link(view, visitor_name):
    visitor_part = f"&visitor={quote_plus(visitor_name)}" if visitor_name else ""
    return f"?view={view}{visitor_part}"


def go_to_view(view, visitor_name):
    st.query_params["view"] = view
    st.query_params["visitor"] = visitor_name
    st.rerun()


def render_home_page(visitor_name):
    event = get_event_date()
    event_str = event.strftime('%Y-%m-%d %H:%M:%S')
    audio_src, audio_available = get_audio_source()

    full_code = f"""
    <style>{get_css()}</style>
    {get_html(audio_src, audio_available, "#")}
    {get_js(event_str, audio_available, "")}
    """

    components.html(full_code, height=820, scrolling=False)

    st.markdown("""
    <style>
    div[data-testid="stButton"] > button[kind="secondary"] {
      position: fixed;
      left: 50%;
      bottom: 18px;
      transform: translateX(-50%);
      min-width: 160px;
      border-radius: 999px;
      border: none;
      background: linear-gradient(180deg, #c88870 0%, #b86e57 100%);
      color: #fffaf7;
      font-weight: 600;
      letter-spacing: 0.04em;
      box-shadow: 0 14px 26px rgba(184, 110, 87, 0.28);
      z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

    # if st.button("Message", key="open_chat_button", type="secondary"):
    #     go_to_view("chat", visitor_name)


def render_chat_html(thread, back_href):
    parts = [
        "<html><head><meta name='viewport' content='width=device-width, initial-scale=1' />",
        "<style>",
        "html,body{margin:0;height:100%;background:#f7efe9;font-family:Outfit,system-ui,sans-serif;color:#2f211d;}",
        "body{overflow:hidden;}",
        ".chat-page{height:100vh;display:flex;flex-direction:column;background:linear-gradient(180deg,#fbf6f2 0%,#f7efe9 100%);} ",
        ".chat-header{display:flex;align-items:center;gap:12px;padding:14px 16px;background:rgba(255,252,249,0.92);backdrop-filter:blur(10px);border-bottom:1px solid rgba(184,110,87,0.12);} ",
        ".back-link{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:999px;background:#f4e5dc;color:#8f5e4d;text-decoration:none;font-size:18px;font-weight:700;}",
        ".chat-title{display:flex;flex-direction:column;gap:2px;}",
        ".chat-title strong{font-size:1rem;color:#2f211d;}",
        ".chat-title span{font-size:0.78rem;color:#8d756b;}",
        ".chat-scroll{flex:1;overflow-y:auto;padding:16px 14px 22px;display:flex;flex-direction:column;gap:10px;scroll-behavior:auto;}",
        ".chat-empty{align-self:center;padding:14px 16px;border-radius:18px;background:#f7f2ee;color:#8b7b73;text-align:center;font-size:0.95rem;max-width:260px;}",
        ".chat-row{display:flex;width:100%;}",
        ".chat-row.left{justify-content:flex-start;}",
        ".chat-row.right{justify-content:flex-end;}",
        ".chat-bubble{max-width:78%;padding:10px 12px 8px;border-radius:18px;box-shadow:0 8px 18px rgba(90,66,58,0.06);} ",
        ".chat-bubble.owner{background:#ffffff;border-top-left-radius:6px;color:#342521;}",
        ".chat-bubble.visitor{background:linear-gradient(180deg,#d7b5a6 0%,#c99079 100%);border-top-right-radius:6px;color:#fffaf7;}",
        ".chat-text{white-space:pre-wrap;word-break:break-word;line-height:1.4;font-size:0.98rem;}",
        ".chat-time{margin-top:6px;font-size:0.72rem;text-align:right;opacity:0.72;}",
        "</style></head><body><div class='chat-page'>",
        f"<div class='chat-header'><a class='back-link' href='{html.escape(back_href)}' target='_top'>&lsaquo;</a><div class='chat-title'><strong>Private chat</strong><span>Telegram connected</span></div></div>",
        "<div id='chat-scroll' class='chat-scroll'>",
    ]

    if not thread:
        parts.append("<div class='chat-empty'>Send a message to the bot and it will appear here.</div>")

    for item in thread:
        direction = item.get("direction", "owner_to_visitor")
        row = "left" if direction == "owner_to_visitor" else "right"
        bubble = "owner" if direction == "owner_to_visitor" else "visitor"
        text = html.escape(item.get("text", ""))
        created_at = item.get("created_at", "")
        time_text = html.escape(created_at[11:16]) if len(created_at) >= 16 else ""
        parts.append(
            f"<div class='chat-row {row}'><div class='chat-bubble {bubble}'><div class='chat-text'>{text}</div><div class='chat-time'>{time_text}</div></div></div>"
        )

    parts.extend([
        "</div>",
        "<script>const el=document.getElementById('chat-scroll'); if(el){el.scrollTop=el.scrollHeight;}</script>",
        "</div></body></html>",
    ])
    return "".join(parts)


def render_chat_page(visitor_name):
    back_href = build_nav_link("home", visitor_name)
    st.markdown("""
    <style>
    .chat-compose-wrap {
      position: sticky;
      bottom: 0;
      background: linear-gradient(180deg, rgba(247,239,233,0) 0%, rgba(247,239,233,0.94) 18%, rgba(247,239,233,1) 100%);
      padding-top: 10px;
      padding-bottom: 6px;
    }
    div[data-testid="stTextInput"] {
      width: 100%;
    }
    div[data-testid="stTextInput"] input {
      border-radius: 999px;
      height: 56px;
      background: #fffaf7;
      color: #2f211d !important;
      -webkit-text-fill-color: #2f211d !important;
      caret-color: #2f211d !important;
      padding-left: 18px;
      padding-right: 18px;
    }
    div[data-testid="stTextInput"] input::placeholder {
      color: #8b7b73;
      -webkit-text-fill-color: #8b7b73;
    }
    div[data-testid="stFormSubmitButton"] {
      margin: 0;
      width: 100%;
    }
    div[data-testid="stFormSubmitButton"] button {
      width: 100%;
      height: 56px;
      border-radius: 999px;
      background: linear-gradient(180deg, #c88870 0%, #b86e57 100%);
      color: white;
      border: none;
      font-weight: 600;
      box-shadow: 0 10px 18px rgba(184, 110, 87, 0.18);
    }
    </style>
    """, unsafe_allow_html=True)

    top_anchor = st.empty()
    if st.button("Back", key="back_home_button"):
        go_to_view("home", visitor_name)

    @st.fragment(run_every="3s")
    def render_chat_messages():
        thread = get_chat_thread(visitor_name)
        components.html(render_chat_html(thread, back_href), height=CHAT_HEIGHT, scrolling=False)

    render_chat_messages()

    with st.container():
        st.markdown("<div class='chat-compose-wrap'>", unsafe_allow_html=True)
        with st.form("reply_form", clear_on_submit=True):
            left_col, right_col = st.columns([5.2, 1.15], vertical_alignment="center")
            with left_col:
                reply = st.text_input(
                    "Reply",
                    label_visibility="collapsed",
                    placeholder=f"Message as {visitor_name}...",
                )
            with right_col:
                submitted = st.form_submit_button("Send")
            if submitted:
                if send_visitor_reply(visitor_name, reply):
                    st.session_state["chat_keep_bottom"] = True
                    st.rerun()
                else:
                    st.error("Could not send the reply to Telegram. Check your app secrets and bot setup.")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.pop("chat_keep_bottom", False):
        components.html("<script>window.parent.scrollTo(0, document.body.scrollHeight);</script>", height=0)


st.set_page_config(page_title="TickTill", page_icon="*", layout="centered")
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

view = st.query_params.get("view", "home")
if isinstance(view, list):
    view = view[0] if view else "home"
view = str(view).strip().lower() or "home"

if view == "chat":
    render_chat_page(visitor_name)
else:
    render_home_page(visitor_name)
