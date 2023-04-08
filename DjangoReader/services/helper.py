import base64
from idlelib.pyparse import trans


def fromBase64(text_source):
    return base64.b64decode(text_source.encode()).decode()


def toBase64(text_source):
    return base64.b64encode(text_source.encode()).decode()
