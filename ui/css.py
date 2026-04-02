import base64

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_base64_image("ui/images/kids.png")

def get_css():
    return f"""
    body {{
      margin: 0;
      background: #f8f5f2;
      font-family: 'Playfair Display', serif;
    }}

    .app {{
      max-width: 420px;
      margin: 20px auto;
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
    """