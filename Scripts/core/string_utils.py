from html import escape
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

        text = re.sub(r"<script[\s\S]*?>[\s\S]*?<\/script>|<style[\s\S]*?>[\s\S]*?<\/style>|<[^>]*>", "", text)
        text = text.replace('&nbsp;', ' ')
        text = re.sub(r'\s+', ' ', text).strip()

        return text