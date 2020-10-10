import os, sys
from unittest import TestCase

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from smoljson import core


class TestLexer(TestCase):
    def test_token_json(self):
        self.assertEqual(core.lexer("{}[]"), ["{", "}", "[", "]"])

    def test_token_whitespace(self):
        self.assertEqual(core.lexer("{ } [ ]"), ["{", "}", "[", "]"])

    def test_token_string(self):
        self.assertEqual(core.lexer('"hello" "there"'), ["hello", "there"])

    def test_token_null(self):
        self.assertEqual(core.lexer("null"), ["null"])

    def test_token_bool(self):
        self.assertEqual(core.lexer("true false"), ["true", "false"])


class TestLexString(TestCase):
    def test_not_string(self):
        self.assertEqual(core.lex_string("{}"), (None, "{}"))

    def test_empty_string(self):
        self.assertEqual(core.lex_string('""'), ("", ""))

    def test_normal_string(self):
        self.assertEqual(core.lex_string('"hello"'), ("hello", ""))

    def test_normal_string_remaining(self):
        self.assertEqual(core.lex_string('"hello" "other"'), ("hello", ' "other"'))

    def test_no_closing_quote_raises_lexical_error(self):
        with self.assertRaisesRegex(
            core.LexicalError, "String closing quote not found"
        ):
            core.lex_string('"hello')


class TestLexNull(TestCase):
    def test_empty_string(self):
        self.assertEqual(core.lex_null(""), (None, ""))

    def test_not_null(self):
        self.assertEqual(core.lex_null("none"), (None, "none"))

    def test_is_null(self):
        self.assertEqual(core.lex_null("null"), ("null", ""))


class TestLexBool(TestCase):
    def test_empty_string(self):
        self.assertEqual(core.lex_bool(""), (None, ""))

    def test_not_bool(self):
        self.assertEqual(core.lex_bool("none"), (None, "none"))

    def test_is_true(self):
        self.assertEqual(core.lex_bool("true"), ("true", ""))

    def test_is_false(self):
        self.assertEqual(core.lex_bool("false"), ("false", ""))
