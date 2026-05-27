from core.time_utils import TimeUtils
from core.text_id_generator import TextIDGenerator


class HTMLBuilder:
    def build(self, feeds):

        latest_update = TimeUtils.to_string(TimeUtils.now())

        carousels = []

        for f in feeds:

            cards = []

            for item in f["items"]:
                anchor = TextIDGenerator.generate(item.date + item.title)

                cards.append(f"""
<div class="card" id="{anchor}">
    <div class="meta">
        <span>{item.date}</span>
    </div>

    <div class="title">
        {item.title}
    </div>
</div>
""")

            carousels.append(f"""
<div class="carousel-section">

    <div class="carousel-header">
        {f['source']}
    </div>

    <div class="carousel">
        {''.join(cards)}
    </div>

</div>
""")

        return f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">

<title>خبر فوری</title>
<link rel="favicon" type="image/x-icon" href="/assets/favicon.webp">

<style>
    @font-face {{
          font-family: Ravi;
          font-style: normal;
          font-weight: normal;
          src: url('https://github.com/shawnkasaei/news-reader-meli/raw/refs/heads/main/Feeds/view/assets/fonts/woff/Ravi-Regular.woff') format('woff'),
               url('https://github.com/shawnkasaei/news-reader-meli/raw/refs/heads/main/Feeds/view/assets/fonts/woff2/Ravi-Regular.woff2') format('woff2');
      }}

      @font-face {{
          font-family: Ravi;
          font-style: normal;
          font-weight: bold;
          src: url('https://github.com/shawnkasaei/news-reader-meli/raw/refs/heads/main/Feeds/view/assets/fonts/woff/Ravi-Bold.woff') format('woff'),
               url('https://github.com/shawnkasaei/news-reader-meli/raw/refs/heads/main/Feeds/view/assets/fonts/woff2/Ravi-Bold.woff2') format('woff2');
      }}

      @font-face {{
          font-family: Ravi;
          font-style: normal;
          font-weight: 950;
          src: url('https://github.com/shawnkasaei/news-reader-meli/raw/refs/heads/main/Feeds/view/assets/fonts/woff/Ravi-ExtraBlack.woff') format('woff'),
               url('https://github.com/shawnkasaei/news-reader-meli/raw/refs/heads/main/Feeds/view/assets/fonts/woff2/Ravi-ExtraBlack.woff2') format('woff2');
      }}
    
    :root {{
        --bg: #161618;
        --panel: #333335;
        --card: #333335;
        --border: #333335;
        --text: #FFFFFF;
        --muted: #818183;
        font-size: 16px;
    }}

    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    body {{
        font-family: "Ravi", sans-serif;
        background: var(--bg);
        color: var(--text);
        padding: 0.75rem;
    }}

    .header {{
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 1rem;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }}

    .header h1 {{
        font-size: 1.35rem;
        font-weight: 700;
    }}

    .header .meta {{
        margin-top: 0.35rem;
        font-size: 0.75rem;
        color: var(--muted);
    }}

    .carousel-section {{
        margin-bottom: 1rem;
    }}

    .carousel-header {{
        font-size: 0.9rem;
        font-weight: 700;
        margin: 0.5rem 0;
        color: var(--text);
    }}

    .carousel {{
        display: flex;
        gap: 0.75rem;
        overflow-x: auto;
        padding-bottom: 0.5rem;
        scroll-snap-type: x mandatory;
    }}

    .carousel::-webkit-scrollbar {{
        display: none;
    }}

    .card {{
        flex: 0 0 80%;
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 0.9rem;
        padding: 0.9rem;
        scroll-snap-align: start;
    }}

    @media (min-width: 700px) {{
        .card {{
            flex: 0 0 45%;
        }}
    }}

    @media (min-width: 900px) {{
        .card {{
            flex: 0 0 30%;
        }}
    }}

    .meta {{
        font-size: 0.75rem;
        color: var(--muted);
        margin-bottom: 0.5rem;
    }}

    .title {{
        font-size: 0.85rem;
        font-weight: 700;
        line-height: 1.7;
        word-break: break-word;
    }}
</style>
</head>

<body>

<div class="header">
    <h1>خبر فوری</h1>
    <div class="meta">
        آخرین بروزرسانی: {latest_update}
    </div>
</div>

{''.join(carousels)}

<div onclick="window.scrollTo({{top:0, behavior:'smooth'}})" style="
    position:fixed;
    bottom:20px;
    left:20px;
    width:55px;
    height:55px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    cursor:pointer;
    font-size:1.2rem;
    font-weight: 600;
    background:rgba(255,255,255,0.02);
    backdrop-filter:blur(10px);
    border:1px solid rgba(255,255,255,0.25);
">بالا</div>

</body>
</html>
"""
