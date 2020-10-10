import os, sys
from unittest import TestCase

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from smoljson import lexer


class TestLexer(TestCase):
    def test_token_json(self):
        self.assertEqual(lexer.lexer("{}[]"), ["{", "}", "[", "]"])

    def test_token_whitespace(self):
        self.assertEqual(lexer.lexer("{ } [ ]"), ["{", "}", "[", "]"])

    def test_token_string(self):
        self.assertEqual(lexer.lexer('"hello" "there"'), ["hello", "there"])

    def test_token_null(self):
        self.assertEqual(lexer.lexer("null"), ["null"])

    def test_token_bool(self):
        self.assertEqual(lexer.lexer("true false"), ["true", "false"])

    def test_token_number(self):
        self.assertEqual(lexer.lexer("[123, 5.0]"), ["[", 123, ",", 5.0, "]"])


class TestLexString(TestCase):
    def test_is_empty(self):
        self.assertEqual(lexer.lex_string('""'), ("", ""))

    def test_is_not_string(self):
        self.assertEqual(lexer.lex_string("{}"), (None, "{}"))

    def test_is_string(self):
        self.assertEqual(lexer.lex_string('"hello"'), ("hello", ""))

    def test_leftover(self):
        self.assertEqual(lexer.lex_string('"hello" "other"'), ("hello", ' "other"'))

    def test_no_closing_quote_raises_lexical_error(self):
        with self.assertRaisesRegex(
            lexer.LexicalError, "String closing quote not found"
        ):
            lexer.lex_string('"hello')


class TestLexNull(TestCase):
    def test_is_empty(self):
        self.assertEqual(lexer.lex_null(""), (None, ""))

    def test_is_not_null(self):
        self.assertEqual(lexer.lex_null("none"), (None, "none"))

    def test_is_null(self):
        self.assertEqual(lexer.lex_null("null"), ("null", ""))

    def test_leftover(self):
        self.assertEqual(lexer.lex_null("null test"), ("null", " test"))


class TestLexBool(TestCase):
    def test_is_empty(self):
        self.assertEqual(lexer.lex_bool(""), (None, ""))

    def test_is_not_bool(self):
        self.assertEqual(lexer.lex_bool("none"), (None, "none"))

    def test_is_true(self):
        self.assertEqual(lexer.lex_bool("true"), ("true", ""))

    def test_is_false(self):
        self.assertEqual(lexer.lex_bool("false"), ("false", ""))

    def test_leftover(self):
        self.assertEqual(lexer.lex_bool("false test"), ("false", " test"))


class TestLexNumber(TestCase):
    def test_is_empty(self):
        self.assertEqual(lexer.lex_number(""), (None, ""))

    def test_is_not_number(self):
        self.assertEqual(lexer.lex_number('"hello"'), (None, '"hello"'))

    def test_is_int(self):
        self.assertEqual(lexer.lex_number("42"), (42, ""))

    def test_is_negative(self):
        self.assertEqual(lexer.lex_number("-1"), (-1, ""))

    def test_is_float(self):
        self.assertEqual(lexer.lex_number("5.0"), (5.0, ""))

    def test_is_exponential_notation(self):
        self.assertEqual(lexer.lex_number("2.99792458e8"), (299792458.0, ""))

    def test_leftover(self):
        self.assertEqual(lexer.lex_number("123 test"), (123, " test"))
