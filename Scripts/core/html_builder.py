class HTMLBuilder:

    def build(self, feeds):

        cards = []

        for f in feeds:

            for i, item in enumerate(f["items"], 1):

                anchor = f"{f['file']}-{i}"

                cards.append(f"""
<div class="card" id="{anchor}">

    <div class="meta">
        <span class="source">{f['source']}</span>
        <span>{item.date}</span>
    </div>

    <div class="content">
        {item.title}
    </div>

</div>
""")

        return f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<title>News Feed</title>

<link rel="stylesheet" href="style.css">
</head>

<body>

<div class="container">

    <div class="header">
        <h1>فید خبری</h1>
        <p>آخرین اخبار به‌روزرسانی شده</p>
    </div>

    <div class="grid">
        {''.join(cards)}
    </div>

</div>

</body>
</html>
"""