import unittest
from unittest.mock import MagicMock, Mock
import toga
import toga_dummy


class TestCoreOptionContainer(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.OptionContainer = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.OptionContainer))

        self.op_container = toga.OptionContainer(factory=self.factory)

    def test_option_container_factory_called(self):
        self.factory.OptionContainer.assert_called_once_with(interface=self.op_container)

    def test_adding_container_invokes_add_content(self):
        widget = MagicMock(specs=toga_dummy.factory.Widget)
        label = 'New Container'

        self.op_container.add(label, widget)
        self.op_container._impl.add_content.assert_called_once_with('New Container', widget._impl)
