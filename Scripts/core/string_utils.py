from html import escape
import html
import re

class StringUtils:

    @staticmethod
    def safe(value):

        if value is None:
            return ""

        return escape(str(value))
    
    @staticmethod
    def truncate_text(text, word_limit):

        if not text:
            return ""

        words = text.split()

        if len(words) <= word_limit:
            return text

        return " ".join(words[:word_limit]) + "..."
    
    @staticmethod
    def remove_html_shenanegans(text):

        if not text:
            return ""

        # 1. Decode HTML entities first (important)
        text = html.unescape(text)

        # 2. Remove script/style blocks completely
        text = re.sub(r"<script[\s\S]*?</script>", "", text, flags=re.IGNORECASE)
        text = re.sub(r"<style[\s\S]*?</style>", "", text, flags=re.IGNORECASE)

        # 3. Remove all HTML tags
        text = re.sub(r"<[^>]*>", "", text)

        # 4. Normalize whitespace (includes &nbsp; after unescape)
        text = re.sub(r"\s+", " ", text).strip()

        return text
    
    @staticmethod
    def detect_lang(text: str) -> str:
        text = text.lower()

        if re.search(r'[\u0600-\u06FF]', text):
            return "fa"
        elif re.search(r'[a-z]', text):
            return "en"

        return None