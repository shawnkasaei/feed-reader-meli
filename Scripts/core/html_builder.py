from datetime import datetime, timezone, timedelta


class HTMLBuilder:

    def _relative_time(self, date_str):
        try:
            # RSS format parse
            dt = datetime.strptime(date_str[:-6], "%a, %d %b %Y %H:%M:%S")
            now = datetime.utcnow()
            diff = now - dt

            minutes = int(diff.total_seconds() / 60)
            hours = int(minutes / 60)

            if minutes < 1:
                return "لحظاتی پیش"
            if minutes < 60:
                return f"{minutes} دقیقه پیش"
            if hours < 24:
                return f"{hours} ساعت پیش"
            return f"{int(hours/24)} روز پیش"

        except:
            return ""

    def build(self, feeds):

        cards = []

        latest_update = datetime.utcnow().strftime("%Y-%m-%d %H:%M")

        for f in feeds:

            for i, item in enumerate(f["items"], 1):

                anchor = f"{f['file']}-{i}"
                relative = self._relative_time(item.date)

                cards.append(f"""
<div class="card" id="{anchor}">

    <div class="meta">
        <span class="source">{f['source']}</span>
        <span>{relative}</span>
    </div>

    <div class="title">
        {item.title}
    </div>

    <div class="content">
        {item.date}
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
        <div class="meta">
            آخرین بروزرسانی: {latest_update}
        </div>
    </div>

    <div class="grid">
        {''.join(cards)}
    </div>

</div>

</body>
</html>
"""