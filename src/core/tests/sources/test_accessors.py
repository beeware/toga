from unittest import TestCase

from toga.sources.accessors import build_accessors, to_accessor


class ToAccessorTests(TestCase):
    def test_simple(self):
        "Simple cases can be converted"
        self.assertEqual(to_accessor('hello'), 'hello')
        self.assertEqual(to_accessor('Hello'), 'hello')
        self.assertEqual(to_accessor('Hello1'), 'hello1')
        self.assertEqual(to_accessor('Hello 1'), 'hello_1')
        self.assertEqual(to_accessor('Hello world'), 'hello_world')
        self.assertEqual(to_accessor('Hello World'), 'hello_world')
        self.assertEqual(to_accessor('Hello World 1'), 'hello_world_1')
        self.assertEqual(to_accessor('Hello World 1!'), 'hello_world_1')
        self.assertEqual(to_accessor('Hello!$@# World!^&*('), 'hello_world')

    def test_whitespace_duplicates(self):
        "Multiple whitespace characters are collapsed, after other substitutions have been performed"
        self.assertEqual(to_accessor('Hello - World'), 'hello_world')

    def test_digit_first(self):
        "A digit-first name can't be automatically generated"
        with self.assertRaises(ValueError):
            to_accessor('101 Dalmations')

    def test_symbols_only(self):
        "A symbol-only name can't be automatically generated"
        with self.assertRaises(ValueError):
            to_accessor('$*(!&*@&^*&^!')


class BuildAccessorsTests(TestCase):
    def test_autoconvert(self):
        "If no accessors are provided, the headings are autoconverted"
        self.assertEqual(
            build_accessors(headings=['First Col', 'Second Col', 'Third Col'], accessors=None),
            ['first_col', 'second_col', 'third_col']
        )

    def test_autoconvert_failure(self):
        "If no accessors are provided, all the headings must be autoconvertable"
        with self.assertRaises(ValueError):
            build_accessors(headings=['1st Col', 'Second Col', 'Third Col'], accessors=None)

    def test_unique_accessors(self):
        "The final accessors must be unique"
        with self.assertRaises(ValueError):
            build_accessors(headings=['Col 1', 'Col - 1', 'Third Col'], accessors=None)

    def test_accessor_list_mismatch(self):
        "The number of headings must match the number of accessors if specified as a list"
        with self.assertRaises(ValueError):
            build_accessors(
                headings=['First Col', 'Second Col', 'Third Col'],
                accessors=['first', 'second']
            )

    def test_manual_accessor_list(self):
        "Accessors can be completely manually specified"
        self.assertEqual(
            build_accessors(
                headings=['First Col', 'Second Col', 'Third Col'],
                accessors=['first', 'second', 'third']
            ),
            ['first', 'second', 'third']
        )

    def test_partial_accessor_list(self):
        "None is interpreted as a default on an accessor override list"
        self.assertEqual(
            build_accessors(
                headings=['First Col', '2nd Col', 'Third Col'],
                accessors=[None, 'second', None]
            ),
            ['first_col', 'second', 'third_col']
        )

    def test_accessor_dict(self):
        "Accessor overrides can be specified as a dictionary"
        self.assertEqual(
            build_accessors(
                headings=['First Col', '2nd Col', 'Third Col'],
                accessors={'2nd Col': 'second'}
            ),
            ['first_col', 'second', 'third_col']
        )
