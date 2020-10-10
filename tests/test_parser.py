import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest import TestCase

from smoljson import parser


class TestParse(TestCase):
    def test_list(self):
        self.assertEqual(
            parser.parse(["[", 123, ",", 456, "]", "test"]), ([123, 456], ["test"])
        )

    def test_nested_list(self):
        self.assertEqual(
            parser.parse(["[", 123, ",", "[", 789, "]", ",", 456, "]", "test"]),
            ([123, [789], 456], ["test"]),
        )

    def test_object(self):
        self.assertEqual(
            parser.parse(["{", "a", ":", 123, "}", "test"]), ({"a": 123}, ["test"])
        )

    def test_nested_object(self):
        self.assertEqual(
            parser.parse(["{", "a", ":", "{", "b", ":", "c", "}", "}", "test"]),
            ({"a": {"b": "c"}}, ["test"]),
        )

    def test_all(self):

        self.assertEqual(
            parser.parse(
                ["[", "{", "a", ":", "[", "b", ",", "c", ",", 123, "]", "}", "]"]
            ),
            ([{"a": ["b", "c", 123]}], []),
        )
