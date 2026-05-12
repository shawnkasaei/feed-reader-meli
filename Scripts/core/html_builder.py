from datetime import datetime, timedelta, timezone

TEHRAN = timezone(timedelta(hours=3, minutes=30))
UTC = timezone.utc


class HTMLBuilder:

    def to_tehran(self, date_str):
        date_str = date_str.strip()

        try:
            # حالت 1: GMT (RFC-like)
            if "GMT" in date_str or "+0000" in date_str:
                dt = datetime.strptime(
                    date_str.replace("GMT", "").strip(),
                    "%a, %d %b %Y %H:%M:%S"
                )

                return dt.replace(tzinfo=UTC).astimezone(TEHRAN)

            # حالت 2: فرمت RSS با +0330 (از قبل Tehran time)
            if "+0330" in date_str:
                cleaned = date_str.replace("+0330", "").strip()

                dt = datetime.strptime(
                    cleaned,
                    "%a, %d %b %Y %H:%M:%S"
                )

                return dt.replace(tzinfo=TEHRAN)

            # حالت 3: فرمت ساده "YYYY-MM-DD HH:MM +0330"
            match = None
            if "+0330" in date_str:
                parts = date_str.split("+")[0].strip()
                dt = datetime.strptime(parts, "%Y-%m-%d %H:%M")
                return dt.replace(tzinfo=TEHRAN)

            # حالت 4: fallback استاندارد
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            return dt.replace(tzinfo=TEHRAN)

        except Exception:
            return datetime.now(TEHRAN)

    def relative(self, dt):
        now = datetime.now(TEHRAN)

        # safety: جلوگیری از naive/aware mismatch
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=TEHRAN)

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