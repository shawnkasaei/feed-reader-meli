from html import escape

from core.time_utils import TimeUtils
from core.text_id_generator import TextIDGenerator


class HTMLBuilder:

    CARD_WORD_LIMIT = 22

    def truncate_text(self, text: str) -> str:

        if not text:
            return ""

        words = text.split()

        if len(words) <= self.CARD_WORD_LIMIT:
            return text

        return " ".join(words[:self.CARD_WORD_LIMIT]) + " ..."

    def safe(self, value):

        if value is None:
            return ""

        return escape(str(value))

    def build_card(self, item):

        title = getattr(item, "title", "")
        content = getattr(item, "content", title)
        date = getattr(item, "date", "")

        preview = self.truncate_text(title)

        anchor = TextIDGenerator.generate(
            str(date) + str(title)
        )

        safe_title = self.safe(title)
        safe_preview = self.safe(preview)
        safe_content = self.safe(content).replace("\n", "<br>")
        safe_date = self.safe(date)

        return f"""
<article
    class="news-card"
    id="{anchor}"
    onclick='openNewsModal(
        `{safe_content}`,
        `{safe_date}`
    )'
>

    <div class="card-background-glow"></div>

    <div class="card-top">

        <div class="card-date">
            {safe_date}
        </div>

    </div>

    <div class="card-content">

        <h3 class="card-title">
            {safe_preview}
        </h3>

    </div>

    <div class="card-bottom">

        <div class="read-more">
            مشاهده کامل خبر
        </div>

    </div>

</article>
"""

    def build_section(self, feed):

        source = self.safe(feed.get("source", "خبرگزاری"))

        cards = []

        for item in feed.get("items", []):
            cards.append(self.build_card(item))

        return f"""
<section class="feed-section">

    <div class="feed-header">

        <div class="feed-title-container">

            <div class="feed-indicator"></div>

            <h2 class="feed-title">
                {source}
            </h2>

        </div>

    </div>

    <div class="feed-carousel">
        {''.join(cards)}
    </div>

</section>
"""

    def build(self, feeds):

        latest_update = TimeUtils.to_string(
            TimeUtils.now()
        )

        sections = []

        for feed in feeds:
            sections.append(
                self.build_section(feed)
            )

        return f"""
<!DOCTYPE html>

<html lang="fa" dir="rtl">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
/>

<title>خبر فوری</title>

<link
    rel="icon"
    type="image/webp"
    href="https://raw.githubusercontent.com/shawnkasaei/news-reader-meli/refs/heads/main/Feeds/view/assets/favicon.webp"
/>

<style>

@font-face {{
    font-family: Peyda;

    src:
        url('https://raw.githubusercontent.com/shawnkasaei/news-reader-meli/refs/heads/main/Feeds/view/assets/fonts/Peyda-Regular.ttf')
        format('truetype');

    font-weight: 400;
}}

@font-face {{
    font-family: Peyda;

    src:
        url('https://raw.githubusercontent.com/shawnkasaei/news-reader-meli/refs/heads/main/Feeds/view/assets/fonts/Peyda-Bold.ttf')
        format('truetype');

    font-weight: 700;
}}

:root {{

    --bg-primary: #050d18;

    --bg-secondary: rgba(255,255,255,0.03);

    --bg-card:
        linear-gradient(
            180deg,
            rgba(255,255,255,0.06),
            rgba(255,255,255,0.025)
        );

    --border:
        rgba(255,255,255,0.08);

    --border-hover:
        rgba(59,130,246,0.35);

    --text-primary: #ffffff;

    --text-secondary: #9fb0c4;

    --accent: #60a5fa;

    --shadow:
        0 10px 30px rgba(0,0,0,0.35);

    --modal-bg:
        linear-gradient(
            180deg,
            rgba(15,20,35,0.98),
            rgba(7,11,20,0.98)
        );
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html {{
    scroll-behavior: smooth;
}}

body {{

    background:
        radial-gradient(
            circle at top,
            rgba(59,130,246,0.12),
            transparent 25%
        ),
        radial-gradient(
            circle at right,
            rgba(147,51,234,0.08),
            transparent 25%
        ),
        var(--bg-primary);

    color: var(--text-primary);

    font-family: Peyda, sans-serif;

    min-height: 100vh;

    overflow-x: hidden;

    -webkit-font-smoothing: antialiased;
}}

body.modal-open {{
    overflow: hidden;
}}

a {{
    color: inherit;
    text-decoration: none;
}}

::-webkit-scrollbar {{
    width: 0;
    height: 0;
}}

.app-header {{

    position: sticky;

    top: 0;

    z-index: 999;

    backdrop-filter: blur(24px);

    background:
        rgba(5,13,24,0.72);

    border-bottom:
        1px solid rgba(255,255,255,0.05);

    padding:
        1rem
        1.2rem;

}}

.header-inner {{

    display: flex;

    align-items: center;

    justify-content: space-between;

    gap: 1rem;
}}

.header-left {{

    display: flex;

    flex-direction: column;

    gap: 0.3rem;
}}

.logo-title {{

    font-size: 1.4rem;

    font-weight: 800;

    letter-spacing: -0.02em;
}}

.logo-subtitle {{

    color: var(--text-secondary);

    font-size: 0.82rem;
}}

.header-right {{

    display: flex;

    align-items: center;

    gap: 0.75rem;
}}

.live-badge {{

    display: flex;

    align-items: center;

    gap: 0.5rem;

    padding:
        0.55rem
        0.9rem;

    border-radius: 999px;

    background:
        rgba(255,255,255,0.05);

    border:
        1px solid rgba(255,255,255,0.08);

        
    color: var(--text-secondary)

    font-size: 0.6rem;
}}

.live-dot {{

    width: 8px;
    height: 8px;

    border-radius: 50%;

    background: #22c55e;

    box-shadow:
        0 0 12px #22c55e;
}}

.main-layout {{

    padding:
        1.3rem;

    display: flex;

    flex-direction: column;

    gap: 2rem;
}}

.hero-banner {{

    position: relative;

    overflow: hidden;

    padding:
        1.6rem;

    border-radius: 32px;

    background:
        linear-gradient(
            135deg,
            rgba(59,130,246,0.14),
            rgba(147,51,234,0.08)
        );

    border:
        1px solid rgba(255,255,255,0.08);

    box-shadow: var(--shadow);
}}

.hero-banner::before {{

    content: "";

    position: absolute;

    width: 300px;
    height: 300px;

    top: -120px;
    left: -120px;

    background:
        radial-gradient(
            circle,
            rgba(59,130,246,0.18),
            transparent 70%
        );
}}

.hero-title {{

    position: relative;

    z-index: 2;

    font-size: 1.7rem;

    font-weight: 800;

    line-height: 1.8;

    margin-bottom: 0.75rem;
}}

.hero-description {{

    position: relative;

    z-index: 2;

    color: var(--text-secondary);

    line-height: 2;

    max-width: 700px;
}}

.feed-section {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.feed-header {{

    display: flex;

    align-items: center;

    justify-content: space-between;
}}

.feed-title-container {{

    display: flex;

    align-items: center;

    gap: 0.75rem;
}}

.feed-indicator {{

    width: 10px;
    height: 10px;

    border-radius: 50%;

    background: var(--accent);

    box-shadow:
        0 0 14px var(--accent);
}}

.feed-title {{

    font-size: 1rem;

    font-weight: 700;
}}

.feed-carousel {{

    display: flex;

    gap: 1rem;

    overflow-x: auto;

    scroll-snap-type: x mandatory;

    padding-bottom: 0.5rem;
}}

.news-card {{

    position: relative;

    flex: 0 0 320px;

    width: 320px;

    height: 240px;

    border-radius: 30px;

    padding: 1.2rem;

    overflow: hidden;

    background: var(--bg-card);

    border:
        1px solid var(--border);

    backdrop-filter: blur(18px);

    scroll-snap-align: start;

    display: flex;

    flex-direction: column;

    justify-content: space-between;

    cursor: pointer;

    transition:
        transform 0.25s ease,
        border 0.25s ease,
        background 0.25s ease;
}}

.news-card:hover {{

    transform:
        translateY(-6px);

    border:
        1px solid var(--border-hover);

    background:
        linear-gradient(
            180deg,
            rgba(255,255,255,0.08),
            rgba(255,255,255,0.03)
        );
}}

.card-background-glow {{

    position: absolute;

    width: 240px;
    height: 240px;

    top: -120px;
    left: -120px;

    background:
        radial-gradient(
            circle,
            rgba(59,130,246,0.16),
            transparent 70%
        );
}}

.card-top,
.card-content,
.card-bottom {{
    position: relative;
    z-index: 2;
}}

.card-date {{

    color: var(--text-secondary);

    font-size: 0.76rem;
}}

.card-content {{
    flex: 1;

    display: flex;

    align-items: center;
}}

.card-title {{

    font-size: 1rem;

    font-weight: 700;

    line-height: 2;

    overflow: hidden;

    display: -webkit-box;

    -webkit-line-clamp: 5;

    -webkit-box-orient: vertical;
}}

.card-bottom {{
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.read-more {{

    color: var(--accent);

    font-size: 0.82rem;

    font-weight: 700;
}}

.modal-overlay {{

    position: fixed;

    inset: 0;

    z-index: 5000;

    display: none;

    align-items: center;

    justify-content: center;

    padding: 1rem;

    background:
        rgba(0,0,0,0.7);

    backdrop-filter: blur(10px);
}}

.modal-overlay.active {{
    display: flex;
}}

.news-modal {{

    position: relative;

    width: 100%;

    max-width: 900px;

    max-height: 92vh;

    overflow-y: auto;

    border-radius: 34px;

    padding: 2rem;

    background: var(--modal-bg);

    border:
        1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 30px 80px rgba(0,0,0,0.45);

    animation:
        modalShow 0.25s ease;
}}

@keyframes modalShow {{

    from {{
        opacity: 0;
        transform:
            translateY(20px)
            scale(0.98);
    }}

    to {{
        opacity: 1;
        transform:
            translateY(0)
            scale(1);
    }}
}}

.modal-close {{

    position: absolute;

    top: 1rem;
    left: 1rem;

    width: 48px;
    height: 48px;

    border-radius: 50%;

    border: 0;

    background:
        rgba(255,255,255,0.06);

    color: white;

    font-size: 1.2rem;

    cursor: pointer;

    transition:
        background 0.2s ease;
}}

.modal-close:hover {{
    background:
        rgba(255,255,255,0.12);
}}

.modal-header {{
    margin-bottom: 1.5rem;
}}

.modal-date {{

    color: var(--text-secondary);

    font-size: 0.85rem;

    margin-bottom: 1rem;
}}

.modal-title {{

    font-size: 1.8rem;

    font-weight: 800;

    line-height: 2;
}}

.modal-content {{

    color: #d7e1ee;

    line-height: 2.4;

    font-size: 1rem;
}}

.scroll-top-btn {{

    position: fixed;

    bottom: 20px;
    left: 20px;

    width: 60px;
    height: 60px;

    border-radius: 50%;

    z-index: 2000;

    display: flex;

    align-items: center;

    justify-content: center;

    cursor: pointer;

    background:
        rgba(255,255,255,0.05);

    backdrop-filter: blur(18px);

    border:
        1px solid rgba(255,255,255,0.08);

    transition:
        transform 0.2s ease,
        background 0.2s ease;
}}

.scroll-top-btn:hover {{

    transform:
        translateY(-4px);

    background:
        rgba(255,255,255,0.08);
}}

@media (max-width: 768px) {{

    .main-layout {{
        padding: 1rem;
    }}

    .hero-banner {{
        border-radius: 26px;
    }}

    .hero-title {{
        font-size: 1.4rem;
    }}

    .news-card {{

        flex: 0 0 85vw;

        width: 85vw;

        height: 230px;
    }}

    .modal-title {{
        font-size: 1.4rem;
    }}

    .news-modal {{
        padding: 1.5rem;
        border-radius: 28px;
    }}
}}

</style>

</head>

<body>

<header class="app-header">

    <div class="header-inner">

        <div class="header-left">

            <div class="logo-title">
                خبر فوری
            </div>

            <div class="logo-subtitle">
                گیت‌هاب
            </div>

        </div>

        <div class="header-right">
            <div class="live-badge">
                <div class="live-dot"></div>

                <!-- زمان اصلی داخل data-time -->
                <span id="latest-update" data-time="{latest_update}">
                    در حال بروزرسانی...
                </span>
            </div>
        </div>

    </div>

</header>

<main class="main-layout">

    <section class="hero-banner">

        <div class="hero-title">
            جدیدترین اخبار روز را سریع‌تر و زیباتر دنبال کنید
        </div>

        <div class="hero-description">
            آخرین انتشارات خبرگزاری‌ها و اندیشکده‌های مطرح جهان رو به روز مطالعه کنید. -شِف
        </div>

    </section>

    {''.join(sections)}

</main>

<div
    class="modal-overlay"
    id="newsModal"
>

    <div class="news-modal">

        <button
            class="modal-close"
            onclick="closeNewsModal()"
        >
            ✕
        </button>

        <div class="modal-header">

            <div
                class="modal-date"
                id="modalDate"
            ></div>

            <div
                class="modal-title"
                id="modalTitle"
            ></div>

        </div>

        <div
            class="modal-content"
            id="modalContent"
        ></div>

    </div>

</div>

<div
    class="scroll-top-btn"
    onclick="scrollToTop()"
>
↑
</div>

<script>

function timeAgo(dateString) {{
    const parts = dateString.split(/[- :]/);

    const date = new Date(
        parts[2],         // year
        parts[1] - 1,     // month
        parts[0],         // day
        parts[3],         // hour
        parts[4],         // minute
        parts[5]          // second
    );

    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);

    if (seconds < 60) {{
        return "چند لحظه پیش";
    }}

    const minutes = Math.floor(seconds / 60);

    if (minutes < 60) {{
        return `${{minutes}} دقیقه پیش`;
    }}

    const hours = Math.floor(minutes / 60);

    if (hours < 24) {{
        return `${{hours}} ساعت پیش`;
    }}

    const days = Math.floor(hours / 24);

    if (days < 30) {{
        return `${{days}} روز پیش`;
    }}

    const months = Math.floor(days / 30);

    if (months < 12) {{
        return `${{months}} ماه پیش`;
    }}

    const years = Math.floor(months / 12);

    return `${{years}} سال پیش`;
}}

const updateElement = document.getElementById("latest-update");
const updateTime = updateElement.dataset.time;

updateElement.textContent = timeAgo(updateTime);

setInterval(() => {{
    updateElement.textContent = timeAgo(updateTime);
}}, 60000);

const modal =
    document.getElementById(
        "newsModal"
    )

function openNewsModal(
    content,
    date
) {{

    document.body.classList.add(
        "modal-open"
    )

    modal.classList.add(
        "active"
    )

    document.getElementById(
        "modalContent"
    ).innerHTML = content

    document.getElementById(
        "modalDate"
    ).innerHTML = date
}}

function closeNewsModal() {{

    document.body.classList.remove(
        "modal-open"
    )

    modal.classList.remove(
        "active"
    )
}}

modal.addEventListener(
    "click",
    function(event) {{

        if(event.target === modal) {{
            closeNewsModal()
        }}
    }}
)

document.addEventListener(
    "keydown",
    function(event) {{

        if(event.key === "Escape") {{
            closeNewsModal()
        }}
    }}
)

function scrollToTop() {{

    window.scrollTo({{
        top: 0,
        behavior: "smooth"
    }})
}}

</script>

</body>

</html>
"""
