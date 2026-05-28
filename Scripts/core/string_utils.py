from html import escape

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