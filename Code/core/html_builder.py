class HTMLBuilder:

    def build(self, feeds):

        cards = []

        for f in feeds:

            for i, item in enumerate(f["items"], 1):

                anchor = f"{f['file']}-{i}"

                cards.append(f"""
<div class="card" id="{anchor}">
    <div class="meta">
        <span>{f['source']}</span>
        <span>{item.date}</span>
    </div>

    <div class="content">{item.title}</div>
</div>
""")

        return f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<title>Feed</title>
<link rel="stylesheet" href="style.css">
</head>

<body>
<div class="container">

<h1>News Feed</h1>

<div class="grid">
{''.join(cards)}
</div>

</div>
</body>
</html>
"""