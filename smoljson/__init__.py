from .lexer import tokenize
from .parser import parse


def load_string(s: str) -> dict:
    """Return JSON dictionary, given some JSON encoded string"""
    tokens = tokenize(s)
    return parse(tokens)[0]
