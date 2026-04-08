import base64
from pathlib import Path


def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


BASE_DIR = Path(__file__).resolve().parent
img_base64 = get_base64_image(BASE_DIR / "images" / "kids.png")


def get_css():
    return f"""
    html, body {{
      margin: 0;
      padding: 0;
      background: transparent;
      font-family: 'Playfair Display', serif;
    }}

    body {{
      display: flex;
      justify-content: center;
      align-items: flex-start;
      padding: 12px 0 32px;
    }}

    .app {{
      position: relative;
      width: 420px;
      max-width: 420px;
      margin: 0 auto;
      background: white;
      border-radius: 24px;
      overflow: hidden;
      box-shadow: 0 20px 50px rgba(0,0,0,0.15);
    }}

    .hero {{
      height: 250px;
      background: url('data:image/png;base64,{img_base64}') center/cover no-repeat;
    }}

    .content {{
      padding: 25px;
      text-align: center;
    }}

    .names {{
      font-size: 26px;
      font-weight: 600;
    }}

    .tagline {{
      font-size: 14px;
      color: #777;
      margin-top: 5px;
    }}

    .date {{
      margin-top: 10px;
      font-size: 16px;
      color: #444;
    }}

    .divider {{
      width: 60px;
      height: 2px;
      background: #ddd;
      margin: 20px auto;
    }}

    .countdown {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 15px;
    }}

    .box {{
      background: #fafafa;
      padding: 15px;
      border-radius: 14px;
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

    .music-btn {{
      position: absolute;
      top: 18px;
      right: 18px;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 52px;
      height: 52px;
      padding: 0;
      appearance: none;
      -webkit-appearance: none;
      background: rgba(255, 255, 255, 0.92);
      border: none;
      outline: none;
      border-radius: 999px;
      color: #4b3b35;
      box-shadow: 0 10px 24px rgba(0,0,0,0.18);
      cursor: pointer;
      z-index: 10;
      transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
    }}

    .music-btn:hover {{
      transform: translateY(-2px);
      box-shadow: 0 14px 28px rgba(0,0,0,0.22);
      background: rgba(255, 255, 255, 1);
    }}

    .music-btn:focus {{
      outline: none;
      box-shadow: 0 10px 24px rgba(0,0,0,0.18);
    }}

    .music-btn:disabled {{
      opacity: 0.55;
      cursor: not-allowed;
      transform: none;
      box-shadow: 0 6px 18px rgba(0,0,0,0.10);
    }}

    .music-icon {{
      font-size: 20px;
      line-height: 1;
    }}
    """
