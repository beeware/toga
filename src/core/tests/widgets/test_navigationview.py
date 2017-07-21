import unittest
from unittest.mock import MagicMock, Mock
import toga
import toga_dummy


class TestCoreNavigationView(unittest.TestCase):
    @unittest.skip('Not implemented!')
    def setUp(self):
        self.factory = MagicMock()
        self.factory.NavigationView = MagicMock(
            return_value=MagicMock(spec=toga_dummy.widgets.navigationview.NavigationView))

        self.title = 'Main View'
        self.content = Mock()
        self.navi_view = toga.NavigationView(self.title,
                                             self.content,
                                             factory=self.factory)

    def test_factory_called(self):
        self.factory.NavigationView.assert_called_once_with(interface=self.navi_view)
