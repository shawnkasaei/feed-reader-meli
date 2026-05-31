import uuid
import hashlib

class TextIDGenerator:

    @staticmethod
    def generate(text: str) -> str:
        text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        unique_id = uuid.uuid4().hex
        return f"{text_hash[:12]}"