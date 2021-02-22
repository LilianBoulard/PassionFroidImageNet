from .utils import validate_fields


# Every image object should have this structure.
image_structure = {
    '_id': str,  # The MongoDB ID.
    'id': str,  # An ID, deduced from its hash.
    'extension': str,  # Type of the image (e.g. "jpg").
    'type': str,
    'product_in': bool,  # Whether a product is shown in the picture.
    'human_in': bool,  # Whether a human is shown in the picture.
    'institutional': bool,  # True if the image is for product, False for ambience.
    'format': bool,  # Format of the picture, True for vertical, False for horizontal.
    'credits': str,  # Name of the original author.
    'limited_usage': bool,  # Whether its use is limited.
    'copyright': bool,  # If the usage is limited, True, False otherwise.
    'usage_end': int,  # Date of end of rights.
    'tags': list,  # A list of tags.
}


def validate_info(func):
    """
    Decorator used to validate the image information passed.
    That way, we can be assured all images have exactly the same information.
    """
    def wrapper(*args, **kwargs):
        if len(args) > 0:
            dictionary = args[0]
        elif len(kwargs) > 0:
            dictionary = kwargs['info']
        else:
            raise ValueError(f"Missing required argument 'info'. ({args}, {kwargs})")
        return func(validate_fields(dictionary, image_structure))
    return wrapper


@validate_info
class Image:

    def __init__(self, info: dict):
        self.set_attributes(info)

    def set_attributes(self, attr: dict):
        for key, value in attr.items():
            self.__setattr__(key, value)
