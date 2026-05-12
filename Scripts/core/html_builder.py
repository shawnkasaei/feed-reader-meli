from datetime import datetime, timedelta, timezone


TEHRAN = timezone(timedelta(hours=3, minutes=30))


class HTMLBuilder:

    def to_tehran(self, date_str):
        if date_str.includes("GMT"):
            try:
                dt = datetime.strptime(
                    date_str.replace("GMT", "").strip(),
                    "%a, %d %b %Y %H:%M:%S"
                )

                return dt.replace(tzinfo=timezone.utc).astimezone(TEHRAN)

            except:
                return datetime.now(TEHRAN)
        else:
            return datetime.strptime(
                    date_str.strip(),
                    "%a, %d %b %Y %H:%M:%S"
                )

    def relative(self, dt):
        now = datetime.now(TEHRAN)
        diff = now - dt

        minutes = int(diff.total_seconds() / 60)
        hours = int(minutes / 60)
        days = int(hours / 24)

        if minutes < 1:
            return "لحظاتی پیش"
        if minutes < 60:
            return f"{minutes} دقیقه پیش"
        if hours < 24:
            return f"{hours} ساعت پیش"
        return f"{days} روز پیش"

    def build(self, feeds):

        cards = []

        latest_update = datetime.now(TEHRAN).strftime("%Y-%m-%d %H:%M")

        for f in feeds:

            for i, item in enumerate(f["items"], 1):

                anchor = f"{f['file']}-{i}"

                dt = self.to_tehran(item.date)
                relative = self.relative(dt)
                tehran_time = dt.strftime("%Y-%m-%d %H:%M")

                cards.append(f"""
<div class="card" id="{anchor}">

    <div class="meta">
        <span>{f['source']}</span>
        <span>{relative}</span>
    </div>

    <div class="title">
        {item.title}
    </div>
<!-- 
    <div class="content">
        {tehran_time}
    </div>
-->
</div> 
""")

        return f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>News Feed</title>
<link rel="stylesheet" href="style.css">
</head>

<body>

<div class="container">

    <div class="header">
        <h1>آخرین خبرها</h1>
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