import unittest
from unittest.mock import MagicMock, Mock
import toga
import toga_dummy


class TestTree(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.Tree = MagicMock(return_value=MagicMock(spec=toga_dummy.widgets.tree.Tree))

        self.heading = ['Heading {}'.format(x) for x in range(3)]
        self.tree = toga.Tree(headings=self.heading,
                              factory=self.factory)

    def test_factory_called(self):
        self.factory.Tree.assert_called_once_with(interface=self.tree)
