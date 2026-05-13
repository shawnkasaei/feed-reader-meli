from collections import defaultdict
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
VIEW_PATH = BASE / "Feeds" / "view"
STYLE_PATH = VIEW_PATH / "style.css"
OUTPUT_PATH = VIEW_PATH / "index.html"


class HTMLBuilder:

    def __init__(self, items):
        self.items = items

    def build(self):
        grouped = defaultdict(list)

        for item in self.items:
            grouped[item.source].append(item)

        style = STYLE_PATH.read_text(encoding="utf-8")

        latest_html = self.render_latest_section(self.items[:20])

        sections_html = ""

        for source, source_items in grouped.items():
            sections_html += self.render_section(source, source_items)

        html = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>News Reader</title>
<style>
{style}
</style>
</head>
<body>

<div class="app">

<header class="header glass">
    <div>
        <h1>خبرخوان</h1>
        <div class="header-meta">
            بروزرسانی: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        </div>
    </div>

    <div class="header-actions">
        <input type="text" id="searchInput" placeholder="جستجو در خبرها...">
    </div>
</header>

<div class="filter-bar" id="filterBar"></div>

{latest_html}

{sections_html}

</div>

<div id="modal" class="modal hidden">
    <div class="modal-overlay" id="modalOverlay"></div>

    <div class="modal-content glass">

        <button class="close-btn" id="closeModal">×</button>

        <div class="modal-source" id="modalSource"></div>

        <h2 id="modalTitle"></h2>

        <div class="modal-body" id="modalBody"></div>

    </div>
</div>

<script>
const cards = document.querySelectorAll('.card')
const modal = document.getElementById('modal')
const modalTitle = document.getElementById('modalTitle')
const modalBody = document.getElementById('modalBody')
const modalSource = document.getElementById('modalSource')
const closeModal = document.getElementById('closeModal')
const modalOverlay = document.getElementById('modalOverlay')
const searchInput = document.getElementById('searchInput')
const filterBar = document.getElementById('filterBar')

const sources = [...new Set([...cards].map(card => card.dataset.source))]

let activeFilter = 'all'

function renderFilters() {{
    filterBar.innerHTML = ''

    const allBtn = document.createElement('button')
    allBtn.textContent = 'همه'
    allBtn.className = 'filter-btn active'
    allBtn.dataset.filter = 'all'
    filterBar.appendChild(allBtn)

    sources.forEach(source => {{
        const btn = document.createElement('button')
        btn.textContent = source
        btn.className = 'filter-btn'
        btn.dataset.filter = source
        filterBar.appendChild(btn)
    }})

    attachFilterEvents()
}}

function attachFilterEvents() {{
    document.querySelectorAll('.filter-btn').forEach(btn => {{

        btn.addEventListener('click', () => {{

            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'))
            btn.classList.add('active')

            activeFilter = btn.dataset.filter

            applyFilters()
        }})
    }})
}}

function applyFilters() {{

    const query = searchInput.value.toLowerCase().trim()

    cards.forEach(card => {{

        const text = card.innerText.toLowerCase()
        const source = card.dataset.source

        const searchMatch = text.includes(query)
        const filterMatch = activeFilter === 'all' || activeFilter === source

        if (searchMatch && filterMatch) {{
            card.style.display = 'flex'
        }} else {{
            card.style.display = 'none'
        }}
    }})
}}

searchInput.addEventListener('input', applyFilters)

cards.forEach(card => {{

    card.addEventListener('click', () => {{

        modalTitle.innerText = card.dataset.title
        modalBody.innerText = card.dataset.content
        modalSource.innerText = card.dataset.source

        modal.classList.remove('hidden')
        document.body.style.overflow = 'hidden'
    }})
}})

function closeModalHandler() {{
    modal.classList.add('hidden')
    document.body.style.overflow = 'auto'
}}

closeModal.addEventListener('click', closeModalHandler)
modalOverlay.addEventListener('click', closeModalHandler)

window.addEventListener('keydown', e => {{
    if (e.key === 'Escape') {{
        closeModalHandler()
    }}
}})

renderFilters()
</script>

</body>
</html>
        """

        OUTPUT_PATH.write_text(html, encoding="utf-8")

    def render_latest_section(self, items):
        cards = ''.join(self.render_card(item) for item in items)

        return f"""
<section class="news-section">

<div class="section-header">
    <h2>آخرین خبرها</h2>
</div>

<div class="carousel">
    {cards}
</div>

</section>
        """

    def render_section(self, source, items):
        cards = ''.join(self.render_card(item) for item in items)

        return f"""
<section class="news-section source-section">

<div class="section-header">
    <h2>{source}</h2>
</div>

<div class="carousel">
    {cards}
</div>

</section>
        """

    def render_card(self, item):
        preview = item.title[:220]

        tags = self.extract_tags(item.title)

        tags_html = ''.join(
            f'<span class="tag">{tag}</span>' for tag in tags
        )

        return f"""
<article
class="card glass"
data-source="{item.source}"
data-title="{item.title.replace('"', '&quot;')}"
data-content="{item.title.replace('"', '&quot;')}"
>

<div class="card-top">
    <span class="source">{item.source}</span>
    <span class="time">{item.relative_time}</span>
</div>

<h3 class="title">{item.title}</h3>

<p class="preview">{preview}</p>

<div class="tags">
    {tags_html}
</div>

</article>
        """

    def extract_tags(self, text):
        tags = []

        keywords = {
            'ایران': 'ایران',
            'ترامپ': 'آمریکا',
            'اسرائیل': 'اسرائیل',
            'جنگ': 'جنگ',
            'اینترنت': 'اینترنت',
            'اقتصاد': 'اقتصاد',
            'ورزش': 'ورزش',
            'فوتبال': 'فوتبال',
            'فناوری': 'فناوری'
        }

        for key, value in keywords.items():
            if key in text:
                tags.append(value)

        return tags[:3]
