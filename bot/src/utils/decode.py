import base64
from io import BytesIO


def decode_image(string: str) -> BytesIO:
    """ Decodes a base64 string into a BytesIO object. """
    decoded_image = base64.b64decode(string)
    image = BytesIO(decoded_image)
    return image
