import os, sys
from unittest import TestCase

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from smoljson import lexer


class TestTokenize(TestCase):
    def test_token_json(self):
        self.assertEqual(lexer.tokenize("{}[]"), ["{", "}", "[", "]"])

    def test_token_whitespace(self):
        self.assertEqual(lexer.tokenize("{ } [ ]"), ["{", "}", "[", "]"])

    def test_token_string(self):
        self.assertEqual(lexer.tokenize('"hello" "there"'), ["hello", "there"])

    def test_token_null(self):
        self.assertEqual(lexer.tokenize("null"), ["null"])

    def test_token_bool(self):
        self.assertEqual(lexer.tokenize("true false"), ["true", "false"])

    def test_token_number(self):
        self.assertEqual(lexer.tokenize("[123, 5.0]"), ["[", 123, ",", 5.0, "]"])


class TestLexString(TestCase):
    def test_is_empty(self):
        self.assertEqual(lexer._string('""'), ("", ""))

    def test_is_not_string(self):
        self.assertEqual(lexer._string("{}"), (None, "{}"))

    def test_is_string(self):
        self.assertEqual(lexer._string('"hello"'), ("hello", ""))

    def test_leftover(self):
        self.assertEqual(lexer._string('"hello" "other"'), ("hello", ' "other"'))

    def test_no_closing_quote_raises_lexical_error(self):
        with self.assertRaisesRegex(
            lexer.LexicalError, "String closing quote not found"
        ):
            lexer._string('"hello')


class TestLexNull(TestCase):
    def test_is_empty(self):
        self.assertEqual(lexer._null(""), (None, ""))

    def test_is_not_null(self):
        self.assertEqual(lexer._null("none"), (None, "none"))

    def test_is_null(self):
        self.assertEqual(lexer._null("null"), ("null", ""))

    def test_leftover(self):
        self.assertEqual(lexer._null("null test"), ("null", " test"))


class TestLexBool(TestCase):
    def test_is_empty(self):
        self.assertEqual(lexer._bool(""), (None, ""))

    def test_is_not_bool(self):
        self.assertEqual(lexer._bool("none"), (None, "none"))

    def test_is_true(self):
        self.assertEqual(lexer._bool("true"), ("true", ""))

    def test_is_false(self):
        self.assertEqual(lexer._bool("false"), ("false", ""))

    def test_leftover(self):
        self.assertEqual(lexer._bool("false test"), ("false", " test"))


class TestLexNumber(TestCase):
    def test_is_empty(self):
        self.assertEqual(lexer._number(""), (None, ""))

    def test_is_not_number(self):
        self.assertEqual(lexer._number('"hello"'), (None, '"hello"'))

    def test_is_int(self):
        self.assertEqual(lexer._number("42"), (42, ""))

    def test_is_negative(self):
        self.assertEqual(lexer._number("-1"), (-1, ""))

    def test_is_float(self):
        self.assertEqual(lexer._number("5.0"), (5.0, ""))

    def test_is_exponential_notation(self):
        self.assertEqual(lexer._number("2.99792458e8"), (299792458.0, ""))

    def test_leftover(self):
        self.assertEqual(lexer._number("123 test"), (123, " test"))
