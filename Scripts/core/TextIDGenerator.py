import uuid
import hashlib

class TextIDGenerator:

    @staticmethod
    def generate(text: str) -> str:
        """
        تولید ID یونیک بر اساس متن + UUID
        """
        # هش کردن متن برای ثبات
        text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()

        # ترکیب با uuid برای یونیک بودن کامل
        unique_id = uuid.uuid4().hex

        return f"{text_hash[:12]}"