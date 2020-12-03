from unittest import TestCase

from toga.sources.row import Row
from toga.sources.stack_source import StackSource


class TestStackSource(TestCase):

    def setUp(self):
        self.one = dict(first="Steven", last="Hawking")
        self.two = dict(first="Albert", last="Einstein")
        self.three = dict(first="Issac", last="Newton")
        self.four = dict(first="Galileo", last="Galilei")

    def assert_rows(self, stack, rows):
        self.assertEqual(len(rows), len(stack))
        for i, row in enumerate(rows):
            self.assertEqual(row, stack[i])

    def test_default_init(self):
        stack = StackSource(accessors=["first", "last"])
        self.assertEqual(0, len(stack))
        self.assertIsNone(stack.size)
        self.assertTrue(stack.unique)

    def test_push(self):
        stack = StackSource(accessors=["first", "last"])
        stack.push(**self.one)
        self.assert_rows(stack, [Row(**self.one)])

    def test_push_multiple_times(self):
        stack = StackSource(accessors=["first", "last"])
        stack.push(**self.one)
        stack.push(**self.two)
        stack.push(**self.three)
        stack.push(**self.four)
        self.assert_rows(
            stack,
            [Row(**self.four), Row(**self.three), Row(**self.two), Row(**self.one)],
        )

    def test_push_with_size_limit(self):
        stack = StackSource(accessors=["first", "last"], size=3)
        stack.push(**self.one)
        stack.push(**self.two)
        stack.push(**self.three)
        stack.push(**self.four)
        self.assert_rows(stack, [Row(**self.four), Row(**self.three), Row(**self.two)])

    def test_same_row_twice_with_uniqueness(self):
        stack = StackSource(accessors=["first", "last"])
        stack.push(**self.one)
        stack.push(**self.two)
        stack.push(**self.three)
        stack.push(**self.four)
        stack.push(**self.two)
        self.assert_rows(
            stack,
            [Row(**self.two), Row(**self.four), Row(**self.three), Row(**self.one)],
        )

    def test_same_row_twice_without_uniqueness(self):
        stack = StackSource(accessors=["first", "last"], unique=False)
        stack.push(**self.one)
        stack.push(**self.two)
        stack.push(**self.three)
        stack.push(**self.four)
        stack.push(**self.two)
        self.assert_rows(
            stack,
            [
                Row(**self.two),
                Row(**self.four),
                Row(**self.three),
                Row(**self.two),
                Row(**self.one),
            ],
        )

    def test_pop(self):
        stack = StackSource(accessors=["first", "last"])
        stack.push(**self.one)
        stack.push(**self.two)
        stack.push(**self.three)
        stack.push(**self.four)
        popped_row = stack.pop()
        self.assertEqual(popped_row, Row(**self.one))
        self.assert_rows(stack, [Row(**self.four), Row(**self.three), Row(**self.two)])
