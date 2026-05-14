from core.time_utils import TimeUtils
from core.text_id_generator import TextIDGenerator


class HTMLBuilder:
    def build(self, feeds):

        latest_update = TimeUtils.to_string(TimeUtils.now())
        carousels = []

        for idx, f in enumerate(feeds):

            carousel_id = f"carousel_{idx}"
            dots_id = f"dots_{idx}"

            items_html = []
            dots_html = []

            items = f["items"]

            for i, item in enumerate(items):
                anchor = TextIDGenerator.generate(item.date + item.title)

                items_html.append(f"""
<div class="card" data-index="{i}" id="{anchor}">
    <div class="meta">{item.date}</div>
    <div class="title">{item.title}</div>
</div>
""")

                dots_html.append(f"""
<span class="dot" onclick="goToSlide('{carousel_id}', {i})"></span>
""")

            carousels.append(f"""
<div class="carousel-section">

    <div class="carousel-header">{f['source']}</div>

    <div class="carousel-wrapper">

        <button class="nav left" onclick="scrollStep('{carousel_id}', -1)">‹</button>

        <div class="carousel" id="{carousel_id}">
            {''.join(items_html)}
        </div>

        <button class="nav right" onclick="scrollStep('{carousel_id}', 1)">›</button>

    </div>

    <div class="dots" id="{dots_id}">
        {''.join(dots_html)}
    </div>

</div>
""")

        return f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>News Feed</title>

<style>
:root {{
    --bg:#161618;
    --card:#2a2a2c;
    --text:#fff;
    --muted:#888;
}}

body {{
    margin:0;
    padding:0.75rem;
    font-family:Ravi,sans-serif;
    background:var(--bg);
    color:var(--text);
}}

.header {{
    padding:1rem;
    background:#222;
    border-radius:1rem;
    margin-bottom:1rem;
}}

.carousel-section {{
    margin-bottom:1.5rem;
}}

.carousel-header {{
    font-weight:700;
    margin-bottom:0.5rem;
}}

.carousel-wrapper {{
    position:relative;
}}

.carousel {{
    display:flex;
    overflow-x:auto;
    scroll-snap-type:x mandatory;
    scroll-behavior:smooth;
    gap:0.75rem;
    padding:0.2rem;
}}

.carousel::-webkit-scrollbar {{
    display:none;
}}

.card {{
    flex:0 0 100%;
    scroll-snap-align:center;
    background:var(--card);
    border-radius:0.9rem;
    padding:1rem;
}}

.meta {{
    font-size:0.75rem;
    color:var(--muted);
    margin-bottom:0.5rem;
}}

.title {{
    font-size:0.9rem;
    font-weight:700;
    line-height:1.6;
}}

.nav {{
    position:absolute;
    top:50%;
    transform:translateY(-50%);
    width:38px;
    height:38px;
    border-radius:50%;
    border:1px solid rgba(255,255,255,0.2);
    background:rgba(255,255,255,0.05);
    backdrop-filter:blur(10px);
    cursor:pointer;
    z-index:10;
}}

.nav.left {{ left:5px; }}
.nav.right {{ right:5px; }}

.dots {{
    display:flex;
    justify-content:center;
    gap:6px;
    margin-top:0.5rem;
}}

.dot {{
    width:6px;
    height:6px;
    border-radius:50%;
    background:#555;
    cursor:pointer;
}}

.dot.active {{
    background:#fff;
}}

</style>
</head>

<body>

<div class="header">
    <h1>آخرین خبرها</h1>
    <div style="color:#888;font-size:0.8rem">
        آخرین بروزرسانی: {latest_update}
    </div>
</div>

{''.join(carousels)}

<div onclick="window.scrollTo({{top:0, behavior:'smooth'}})" style="
    position:fixed;
    bottom:20px;
    right:20px;
    width:50px;
    height:50px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.2);
">
↑
</div>

<script>

function getCardWidth(carousel) {{
    return carousel.querySelector('.card').offsetWidth + 12;
}}

// One-card step scroll
function scrollStep(id, dir) {{
    const el = document.getElementById(id);
    const w = getCardWidth(el);
    el.scrollBy({{ left: dir * w, behavior: 'smooth' }});
}}

// Go to exact slide
function goToSlide(id, index) {{
    const el = document.getElementById(id);
    const w = getCardWidth(el);
    el.scrollTo({{ left: index * w, behavior: 'smooth' }});
}}

// Update dots
function updateDots(carousel, containerId) {{
    const index = Math.round(carousel.scrollLeft / getCardWidth(carousel));
    const dots = document.getElementById(containerId).children;

    for (let i = 0; i < dots.length; i++) {{
        dots[i].classList.remove('active');
    }}

    if (dots[index]) dots[index].classList.add('active');
}}

// Attach scroll listeners
document.querySelectorAll('.carousel').forEach((carousel, i) => {{
    const dotsId = 'dots_' + i;

    carousel.addEventListener('scroll', () => {{
        updateDots(carousel, dotsId);
        handleInfiniteLoop(carousel);
    }});

    // init first dot
    setTimeout(() => {{
        const dots = document.getElementById(dotsId)?.children;
        if (dots?.length) dots[0].classList.add('active');
    }}, 100);
}});

// Infinite loop (simple clone-based)
function handleInfiniteLoop(carousel) {{
    const maxScroll = carousel.scrollWidth - carousel.clientWidth;

    if (carousel.scrollLeft >= maxScroll - 10) {{
        carousel.scrollTo({{ left: 0, behavior: 'auto' }});
    }}
}}

// Auto scroll (pause on hover)
document.querySelectorAll('.carousel').forEach(carousel => {{
    let interval = setInterval(() => {{
        carousel.scrollBy({{ left: getCardWidth(carousel), behavior: 'smooth' }});
    }}, 4000);

    carousel.addEventListener('mouseenter', () => clearInterval(interval));
}});

</script>

</body>
</html>
"""