import json
import base64
import logging

from PIL import Image
from io import BytesIO
from hashlib import sha256

from .config import SALT


def validate_fields(dictionary: dict, struct: dict) -> dict:
    """
    Takes a dictionary and an architecture and checks if the types and structure are valid.
    Corrects the dictionary if necessary. The output dict is valid.
    Recursive only in dictionaries. All other types are not iterated through (e.g. lists).

    Example arch: {"content": str, "meta": {"time_sent": int, "digest": str, "aes": str}}

    :param dict dictionary: A dictionary to check.
    :param dict struct: Dictionary containing the levels of architecture.
    """

    def is_int(value) -> bool:
        """
        Tests a value to check if it is an integer or not.
        """
        try:
            int(value)
        except ValueError:
            return False
        else:
            return True

    if not isinstance(dictionary, dict):
        logging.error(f"Argument 'dictionary' needs to be a dict, is {type(dictionary)}: {dictionary}")
        return dictionary
    if not isinstance(struct, dict):
        logging.error(f"Argument 'struct' needs to be a dict, is {type(struct)}: {struct}")
        return dictionary

    for key, struct_value in struct.items():
        if key not in dictionary:
            if isinstance(struct_value, dict):
                dictionary[key] = struct_value
            else:
                # `struct_value` is a `type` object
                # We therefore create a new instance
                dictionary[key] = struct_value()
            continue
        else:
            dict_value = dictionary[key]

        if isinstance(struct_value, type):
            # If value is a type object, we want to check that the value from the dict is of this type.
            if struct_value is int:
                if not is_int(dict_value):
                    logging.warning(f"Couldn't cast to int {key!r}: {dict_value!r}")
                    dictionary[key] = 0
        elif isinstance(struct_value, dict):
            # If value is a dict, we want to call this function recursively.
            dictionary[key] = validate_fields(dict_value, struct_value)

    if len(dictionary) != len(struct):
        difference = set(dictionary.keys()).symmetric_difference(set(struct.keys()))
        logging.warning(f'Leftover fields in the dictionary: {difference}')
        for dif in difference:
            print(f"{dif}={dictionary[dif]}")

    return dictionary


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
