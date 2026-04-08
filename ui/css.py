import base64
from pathlib import Path


def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


BASE_DIR = Path(__file__).resolve().parent
img_base64 = get_base64_image(BASE_DIR / "images" / "kids.png")


def get_css():
    return f"""
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Outfit:wght@300;400;500;600&family=Playfair+Display:wght@600;700&display=swap');

    :root {{
      --text: #2f211d;
      --muted: #85706a;
      --accent: #b78474;
      --shadow: 0 22px 50px rgba(108, 72, 59, 0.16);
      --shell-pad-x: clamp(6px, 2.5vw, 12px);
      --shell-pad-top: clamp(6px, 2.2vw, 12px);
      --shell-pad-bottom: clamp(12px, 4vw, 22px);
      --card-radius: clamp(24px, 6vw, 30px);
      --hero-height: clamp(220px, 56vw, 290px);
      --content-pad-x: clamp(16px, 4.8vw, 24px);
      --content-pad-y: clamp(18px, 5vw, 26px);
      --title-size: clamp(2rem, 8vw, 2.7rem);
      --tagline-size: clamp(0.88rem, 3.2vw, 1rem);
      --date-size: clamp(0.88rem, 3.3vw, 1rem);
      --number-size: clamp(2rem, 8vw, 2.35rem);
      --label-size: clamp(0.62rem, 2.2vw, 0.72rem);
      --button-size: clamp(44px, 12vw, 50px);
      --countdown-gap: clamp(10px, 3vw, 14px);
      --countdown-pad-y: clamp(14px, 4vw, 18px);
      --countdown-pad-x: clamp(10px, 3vw, 14px);
    }}

    html, body {{
      margin: 0;
      padding: 0;
      background: transparent;
    }}

    body {{
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      padding: var(--shell-pad-top) 0 var(--shell-pad-bottom);
      font-family: 'Outfit', sans-serif;
    }}

    .shell {{
      width: min(100%, 430px);
      padding: 0 var(--shell-pad-x);
      box-sizing: border-box;
    }}

    .app {{
      position: relative;
      width: 100%;
      background: linear-gradient(180deg, rgba(255,255,255,0.99) 0%, rgba(255,250,247,0.99) 100%);
      border-radius: var(--card-radius);
      overflow: hidden;
      box-shadow: var(--shadow);
      opacity: 0;
      transform: translateY(20px) scale(0.985);
      animation: app-reveal 900ms cubic-bezier(0.22, 1, 0.36, 1) forwards;
    }}

    .hero {{
      position: relative;
      height: var(--hero-height);
      background: url('data:image/png;base64,{img_base64}') center top/cover no-repeat;
      transform-origin: center center;
      animation: hero-drift 16s ease-in-out infinite alternate;
    }}

    .hero-overlay {{
      position: absolute;
      inset: 0;
      background:
        linear-gradient(180deg, rgba(66, 40, 36, 0.02) 0%, rgba(66, 40, 36, 0.16) 100%),
        linear-gradient(180deg, rgba(255,255,255,0) 56%, rgba(255,250,247,0.96) 100%);
    }}

    .telegram-popup {{
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
      background: rgba(45, 29, 26, 0.36);
      backdrop-filter: blur(4px);
      z-index: 20;
      opacity: 0;
      pointer-events: none;
      transition: opacity 240ms ease;
    }}

    .telegram-popup.is-visible {{
      opacity: 1;
      pointer-events: auto;
    }}

    .telegram-popup-card {{
      position: relative;
      width: min(100%, 290px);
      padding: 26px 22px 22px;
      border-radius: 22px;
      background: linear-gradient(180deg, rgba(255,248,245,0.98) 0%, rgba(255,252,250,0.98) 100%);
      box-shadow: 0 20px 40px rgba(61, 36, 33, 0.18);
      text-align: center;
      transform: translateY(16px) scale(0.96);
      transition: transform 260ms cubic-bezier(0.22, 1, 0.36, 1);
    }}

    .telegram-popup.is-visible .telegram-popup-card {{
      transform: translateY(0) scale(1);
    }}

    .telegram-popup-close {{
      position: absolute;
      top: 10px;
      right: 10px;
      width: 28px;
      height: 28px;
      border: none;
      border-radius: 999px;
      background: rgba(111, 81, 72, 0.08);
      color: #6f5148;
      font-size: 18px;
      line-height: 1;
      cursor: pointer;
    }}

    .telegram-popup-label {{
      font-size: 11px;
      letter-spacing: 0.24em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 12px;
    }}

    .telegram-popup-text {{
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.9rem;
      line-height: 1.05;
      color: #2d1d1a;
      text-wrap: balance;
    }}

    .content {{
      position: relative;
      padding: var(--content-pad-y) var(--content-pad-x);
      margin-top: clamp(-10px, -2vw, -6px);
      text-align: center;
      color: var(--text);
    }}

    .eyebrow,
    .names,
    .tagline,
    .date-pill,
    .divider {{
      opacity: 0;
      transform: translateY(14px);
      animation: fade-up 720ms cubic-bezier(0.22, 1, 0.36, 1) forwards;
    }}

    .eyebrow {{ font-size: clamp(10px, 2.8vw, 11px); letter-spacing: 0.28em; text-transform: uppercase; color: var(--accent); margin-bottom: clamp(8px, 2vw, 10px); animation-delay: 120ms; }}
    .names {{ font-family: 'Cormorant Garamond', serif; font-size: var(--title-size); line-height: 0.94; font-weight: 700; letter-spacing: 0.01em; margin: 0; text-wrap: balance; animation-delay: 220ms; }}
    .tagline {{ margin-top: clamp(8px, 2vw, 10px); font-size: var(--tagline-size); color: var(--muted); text-wrap: balance; animation-delay: 320ms; }}
    .date-pill {{ display: inline-flex; align-items: center; justify-content: center; margin-top: clamp(14px, 4vw, 18px); padding: clamp(9px, 2.5vw, 11px) clamp(14px, 4vw, 20px); border-radius: 999px; background: linear-gradient(180deg, #fff5ef 0%, #f7ebe4 100%); color: #6f5148; font-size: var(--date-size); box-shadow: inset 0 1px 0 rgba(255,255,255,0.85); animation-delay: 420ms; }}
    .divider {{ width: clamp(62px, 18vw, 74px); height: 1px; background: linear-gradient(90deg, rgba(183,132,116,0) 0%, rgba(183,132,116,0.8) 50%, rgba(183,132,116,0) 100%); margin: clamp(16px, 4vw, 20px) auto; animation-delay: 520ms; }}

    .countdown {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--countdown-gap); }}
    .box {{ padding: var(--countdown-pad-y) var(--countdown-pad-x); border-radius: clamp(16px, 5vw, 20px); background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(249,244,240,0.98) 100%); border: 1px solid rgba(183, 132, 116, 0.08); box-shadow: inset 0 1px 0 rgba(255,255,255,0.95), 0 8px 18px rgba(125, 91, 79, 0.05); opacity: 0; transform: translateY(18px); animation: fade-up 700ms cubic-bezier(0.22, 1, 0.36, 1) forwards; }}
    .box:nth-child(1) {{ animation-delay: 620ms; }}
    .box:nth-child(2) {{ animation-delay: 720ms; }}
    .box:nth-child(3) {{ animation-delay: 820ms; }}
    .box:nth-child(4) {{ animation-delay: 920ms; }}
    .accent-box {{ background: linear-gradient(180deg, #fff6f1 0%, #f9ebe4 100%); }}
    .number {{ display: inline-block; font-family: 'Playfair Display', serif; font-size: var(--number-size); font-weight: 700; line-height: 1; color: #241714; transition: transform 220ms ease, opacity 220ms ease, filter 220ms ease; }}
    .number.tick {{ animation: number-tick 360ms ease; }}
    .label {{ margin-top: 6px; font-size: var(--label-size); color: #8c746d; letter-spacing: 0.24em; }}

    .music-btn {{ position: absolute; top: clamp(12px, 3.5vw, 16px); right: clamp(12px, 3.5vw, 16px); display: flex; align-items: center; justify-content: center; width: var(--button-size); height: var(--button-size); padding: 0; appearance: none; -webkit-appearance: none; -webkit-tap-highlight-color: transparent; background: rgba(255, 255, 255, 0.84); border: none; outline: none; border-radius: 999px; color: #4b3b35; box-shadow: 0 10px 22px rgba(84, 57, 50, 0.14); backdrop-filter: blur(10px); cursor: pointer; z-index: 10; transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease; }}
    .music-btn:hover {{ transform: translateY(-2px); box-shadow: 0 14px 28px rgba(84, 57, 50, 0.18); background: rgba(255, 255, 255, 0.92); }}
    .music-btn:focus, .music-btn:active {{ outline: none; border: none; box-shadow: 0 10px 22px rgba(84, 57, 50, 0.14); }}
    .music-btn:disabled {{ opacity: 0.55; cursor: not-allowed; transform: none; box-shadow: 0 6px 18px rgba(0,0,0,0.10); }}
    .music-btn.loading {{ cursor: progress; }}
    .music-btn.playing {{ animation: music-pulse 2.2s ease-in-out infinite; }}
    .music-icon {{ display: flex; align-items: center; justify-content: center; width: clamp(18px, 4.8vw, 20px); height: clamp(18px, 4.8vw, 20px); font-size: clamp(16px, 4.4vw, 18px); line-height: 1; }}
    .music-btn.loading .music-icon {{ width: clamp(16px, 4.2vw, 18px); height: clamp(16px, 4.2vw, 18px); border: 2px solid rgba(75, 59, 53, 0.22); border-top-color: #4b3b35; border-radius: 50%; animation: music-spin 0.8s linear infinite; font-size: 0; }}

    @keyframes app-reveal {{ to {{ opacity: 1; transform: translateY(0) scale(1); }} }}
    @keyframes fade-up {{ to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes hero-drift {{ from {{ transform: scale(1) translateY(0); }} to {{ transform: scale(1.045) translateY(-4px); }} }}
    @keyframes number-tick {{ 0% {{ transform: translateY(0); opacity: 1; filter: blur(0); }} 40% {{ transform: translateY(-4px); opacity: 0.72; filter: blur(0.3px); }} 100% {{ transform: translateY(0); opacity: 1; filter: blur(0); }} }}
    @keyframes music-spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    @keyframes music-pulse {{ 0%, 100% {{ box-shadow: 0 10px 22px rgba(84, 57, 50, 0.14); transform: scale(1); }} 50% {{ box-shadow: 0 0 0 10px rgba(183, 132, 116, 0.08), 0 12px 24px rgba(84, 57, 50, 0.18); transform: scale(1.02); }} }}

    @media (prefers-reduced-motion: reduce) {{
      .app, .hero, .eyebrow, .names, .tagline, .date-pill, .divider, .box, .music-btn.playing, .number.tick {{
        animation: none !important; transition: none !important; transform: none !important; opacity: 1 !important;
      }}
      .telegram-popup, .telegram-popup-card {{ transition: none !important; }}
    }}

    @media (max-width: 340px) {{ .shell {{ padding-left: 4px; padding-right: 4px; }} .content {{ padding-left: 14px; padding-right: 14px; }} .label {{ letter-spacing: 0.18em; }} .telegram-popup-card {{ padding: 24px 18px 18px; }} .telegram-popup-text {{ font-size: 1.65rem; }} }}
    @media (max-height: 740px) and (orientation: landscape) {{ :root {{ --hero-height: clamp(180px, 42vw, 220px); --title-size: clamp(1.75rem, 4vw, 2.1rem); --number-size: clamp(1.5rem, 4vw, 1.9rem); }} body {{ padding-top: 8px; padding-bottom: 16px; }} .shell {{ width: min(100%, 520px); }} .content {{ padding-top: 16px; padding-bottom: 18px; }} .countdown {{ gap: 10px; }} .box {{ padding-top: 12px; padding-bottom: 12px; }} }}
    """