import re
from typing import List, Tuple, Optional


TOKENS_WHITESPACE = set([" ", "\n", "\r" "\t"])

TOKENS_ARRAY = set(["[", "]", ","])
TOKENS_OBJECT = set(["{", "}", ":"])
TOKENS_JSON = TOKENS_ARRAY.union(TOKENS_OBJECT)

TOKEN_NULL = "null"
TOKEN_FALSE = "false"
TOKEN_TRUE = "true"
TOKEN_QUOTE = '"'

REGEX_NUMBER = re.compile(
    pattern=r"""
    -?                # optional negative sign
    (?:0|[1-9]\d*)    # starts with 0 digit OR 1-9 digit followed by 0+ digits
    (?:\.\d+)?        # optional decimal followed by 1+ digits
    (?:[eE][-+]?\d+)? # optional exponential notation
    """,
    flags=re.VERBOSE,
)


class LexicalError(ValueError):
    pass


def lexer(s: str) -> List[str]:
    tokens = []
    while len(s):
        token, s = lex_string(s)
        if token is not None:
            tokens.append(token)
            continue

        token, s = lex_null(s)
        if token is not None:
            tokens.append(token)
            continue

        token, s = lex_bool(s)
        if token is not None:
            tokens.append(token)
            continue

        token, s = lex_number(s)
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


def lex_string(s: str) -> Tuple[Optional[str], str]:
    """Return first string, if it exists"""
    if s[0] == TOKEN_QUOTE:
        for i, c in enumerate(s[1:], start=1):
            if c == TOKEN_QUOTE:
                return s[1:i], s[i + 1 :]
        raise LexicalError("String closing quote not found")
    else:
        return None, s


def lex_null(s: str) -> Tuple[Optional[str], str]:
    """Return 'null' if it exists"""
    n = len(TOKEN_NULL)
    if s[:n] == TOKEN_NULL:
        return s[:n], s[n:]
    else:
        return None, s


def lex_bool(s: str) -> Tuple[Optional[str], str]:
    """Return 'true' or 'false' if they exist"""
    n = len(TOKEN_FALSE)
    if s[:n] == TOKEN_FALSE:
        return s[:n], s[n:]
    n = len(TOKEN_TRUE)
    if s[:n] == TOKEN_TRUE:
        return s[:n], s[n:]
    return None, s


def lex_number(s: str) -> Tuple[Optional[str], str]:
    """Return number if it exists"""
    match = REGEX_NUMBER.match(s)
    if match is not None:
        number = match[0]
        if "." in number:
            return float(number), s[len(number) :]
        else:
            return int(number), s[len(number) :]
    return None, s
