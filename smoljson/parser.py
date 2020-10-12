from typing import List, Tuple, Any


class ParserError(Exception):
    """Raised if there is an error while parsing"""

    pass


def parse(tokens: List[str]):
    """Return JSON dict from tokens"""
    if not tokens:
        raise ParserError("Expected value")
    t = tokens[0]
    if t == "[":
        return _list(tokens[1:])
    if t == "{":
        return _object(tokens[1:])
    return t, tokens[1:]


def _list(tokens: List):
    """Return python list from tokens"""
    t = tokens[0]
    ls = []
    if t == "]":
        return ls, tokens[1:]
    while len(tokens):
        val, tokens = parse(tokens)
        ls.append(val)
        t = tokens[0]
        if t == "]":
            return ls, tokens[1:]
        if t != ",":
            raise ParserError("Expected ',' after list value")
        tokens = tokens[1:]
    raise ParserError("Expected ']' value to close list")


def _object(tokens: List):
    """return python dict from tokens"""
    t = tokens[0]
    _dict = {}
    if t == "}":
        return _dict, tokens[1:]
    while len(tokens):
        key = tokens[0]
        if not isinstance(key, str):
            raise ParserError(f"Excepted string key, got: {key}")
        tokens = tokens[1:]
        t = tokens[0]
        if t != ":":
            raise ParserError(f"Expected colon after key, got: {t}")
        val, tokens = parse(tokens[1:])
        _dict[key] = val
        t = tokens[0]
        if t == "}":
            return _dict, tokens[1:]
        if t != ",":
            raise ParserError(f"Expected comma after value, got: {t}")
        tokens = tokens[1:]
    raise ParserError("Expected '}' value to close object")
