import base64
import json
import random
from django.conf import settings


def parse_id_token(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        return False
    payload = parts[1]
    padded = payload + '=' * (4 - len(payload) % 4)
    decoded = base64.b64decode(padded)
    return json.loads(decoded)


def set_random_image():
    images = ['default.jpg', 'joda.jpeg', 'wiedzmin.jpg']
    return 'http://127.0.0.1:8000/media/' + random.choice(images)

