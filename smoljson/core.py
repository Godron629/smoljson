from typing import List, Tuple, Optional


TOKENS_WHITESPACE = set([" ", "\n", "\r" "\t"])

TOKENS_ARRAY = set(["[", "]", ","])
TOKENS_OBJECT = set(["{", "}", ":"])
TOKENS_JSON = TOKENS_ARRAY.union(TOKENS_OBJECT)

TOKEN_NULL = "null"
TOKEN_FALSE = "false"
TOKEN_TRUE = "true"
TOKEN_QUOTE = '"'


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

        ...

        # change to using i so no string reassign

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
    negative = False
    leading_zero = False
    digits = set(range(10))
    while len(s): 
        if s[0] == "-": 
            if negative: 
                raise LexicalError("Double minus")
            negative = True
            s = s[1:]
            continue
        if s[0] == "0": 
            leading_zero = True
            s = s[1:]
            continue
        if s[0] in digits: 
            pass



