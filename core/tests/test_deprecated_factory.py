import toga
from toga_dummy.utils import TestCase


class DeprecatedFactoryTests(TestCase):
    def setUp(self):
        super().setUp()
        self.factory = object()
        self.callback = lambda x: None

    ######################################################################
    # 2022-09: Backwards compatibility
    ######################################################################
    # factory no longer used

    def test_app(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.App(
                formal_name="Test", app_id="org.beeware.test-app", factory=self.factory
            )
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_document_app(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.DocumentApp(
                formal_name="Test", app_id="org.beeware.test-app", factory=self.factory
            )
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_command(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Command(self.callback, "Test", factory=self.factory)
        with self.assertWarns(DeprecationWarning):
            widget.bind(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_command_set(self):
        with self.assertWarns(DeprecationWarning):
            toga.CommandSet(factory=self.factory)

    ######################################################################
    # End backwards compatibility.
    ######################################################################
