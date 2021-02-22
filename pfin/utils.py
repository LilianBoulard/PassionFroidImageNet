import json
import base64

from PIL import Image
from io import BytesIO
from hashlib import sha256

from .config import SALT


def hash_password(password: str) -> str:
    """
    Takes a clear-text password and returns it salted and hashed.
    """
    h = sha256()
    h.update(SALT + password.encode())
    return h.hexdigest()


def encode_base64(image: Image) -> str:
    """
    Takes a PIL image and returns its base64 value.
    """
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


def encode_json(dictionary: dict) -> str:
    """
    Takes a dictionary and returns a JSON-encoded string.

    :param dict dictionary: A dictionary.
    :return str: A JSON-encoded string.
    """
    return json.JSONEncoder().encode(dictionary)


def decode_json(json_string: str) -> dict:
    """
    Takes a message as a JSON string and unpacks it to get a dictionary.

    :param str json_string: A message, as a JSON string.
    :return dict: An unverified dictionary. Do not trust this data.
    """
    return json.JSONDecoder().decode(json_string)
