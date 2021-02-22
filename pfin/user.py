import flask_login
from .utils import validate_fields

# Every user object should have this structure.
user_structure = {
    '_id': str,  # The MongoDB ID.
    'name': str,  # The displayed name.
    'email': str,  # The user's email address.
    'password': str,  # Salted and hashed password.
    'group': str,  # The group it is part of. Can be any of {'guest', 'regional', 'national'}
}


def validate_info(func):
    """
    Decorator used to validate the user information passed.
    That way, we can be assured all users have exactly the same information.
    """
    def wrapper(*args, **kwargs):
        if len(args) > 0:
            dictionary = args[0]
        elif len(kwargs) > 0:
            dictionary = kwargs['info']
        else:
            raise ValueError(f"Missing required argument 'info'. ({args}, {kwargs})")
        nice_structure = validate_fields(dictionary, user_structure)
        return func(nice_structure)
    return wrapper


@validate_info
class User:

    def __init__(self, info: dict):
        self.set_attributes(info)

    def set_attributes(self, attr: dict):
        for key, value in attr.items():
            self.__setattr__(key, value)


class DummyUser(flask_login.UserMixin):
    pass
