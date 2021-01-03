from unittest import TestCase

from toga.sources.row import Row


class RowTests(TestCase):
    def test_hashable(self):
        row = Row(a=1, b=2)

        data = {
            row: 'value',
        }

        assert data[row] == 'value'

    def test_equality(self):
        row1 = Row(a=1, b=2)
        row2 = Row(a=1, b=2)
        row3 = Row(a=2, c=3)

        data = {
            row1: 'value',
        }

        # Equality is based on value.
        assert row1 == row2
        assert row2 != row3

        # Lookup is also based on equality.
        assert data[row2] == 'value'
