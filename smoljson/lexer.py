from typing import List, Tuple, Optional

from smoljson import util


TOKENS_WHITESPACE = set([" ", "\n", "\r" "\t"])

TOKENS_ARRAY = set(["[", "]", ","])
TOKENS_OBJECT = set(["{", "}", ":"])
TOKENS_JSON = TOKENS_ARRAY.union(TOKENS_OBJECT)

TOKEN_NULL = "null"
TOKEN_FALSE = "false"
TOKEN_TRUE = "true"
TOKEN_QUOTE = '"'


class LexicalError(ValueError):
    """Raised if character found while tokenizing is invalid"""

    pass


def tokenize(s: str) -> List[str]:
    """Return list of JSON tokens from a string - no whitespace included"""
    tokens = []
    while len(s):
        token, s = _string(s)
        if token is not None:
            tokens.append(token)
            continue

        token, s = _null(s)
        if token is True:
            # None means no token found, except the token _is_ `None`. To be
            # consistent `_null` returns True if token is found, None otherwise.
            tokens.append(None)
            continue

        token, s = _bool(s)
        if token is not None:
            tokens.append(token)
            continue

        token, s = _number(s)
        if token is not None:
            tokens.append(token)
            continue

        if s[0] in TOKENS_ARRAY:
            tokens.append(s[0])
            s = s[1:]
            continue

        if s[0] in TOKENS_OBJECT:
            tokens.append(s[0])
            s = s[1:]
            continue

        if s[0] in TOKENS_WHITESPACE:
            s = s[1:]
            continue

        raise LexicalError(f"Unexpected character: {s[0]}")

    return tokens


def _string(s: str) -> Tuple[Optional[str], str]:
    """Return first string token it exists"""
    if s[0] == TOKEN_QUOTE:
        for i, c in enumerate(s[1:], start=1):
            if c == TOKEN_QUOTE:
                return s[1:i], s[i + 1 :]
        raise LexicalError("String closing quote not found")
    else:
        return None, s


def _null(s: str) -> Tuple[Optional[str], str]:
    """Return first null token if it exists"""
    n = len(TOKEN_NULL)
    if s[:n] == TOKEN_NULL:
        return True, s[n:]
    else:
        return None, s


def _bool(s: str) -> Tuple[Optional[str], str]:
    """Return first bool token if it exists"""
    n = len(TOKEN_FALSE)
    if s[:n] == TOKEN_FALSE:
        return False, s[n:]
    n = len(TOKEN_TRUE)
    if s[:n] == TOKEN_TRUE:
        return True, s[n:]
    return None, s


def _number(s: str) -> Tuple[Optional[str], str]:
    """Return first number token if it exists"""
    match = util.REGEX_NUMBER.match(s)
    if match is not None:
        number = match[0]
        if "." in number:
            return float(number), s[len(number) :]
        else:
            return int(number), s[len(number) :]
    return None, s
