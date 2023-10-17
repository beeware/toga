import asyncio
from pathlib import Path
from unittest.mock import Mock

import toga
from toga.widgets.base import WidgetRegistry
from toga_dummy.utils import TestCase


class AppTests(TestCase):
    def setUp(self):
        super().setUp()

        self.name = "Test App"
        self.app_id = "org.beeware.test-app"
        self.id = "dom-id"

        self.content = Mock()
        self.content_id = "content-id"
        self.content.id = self.content_id

        self.started = False

        def test_startup_function(app):
            self.started = True
            return self.content

        self.app = toga.App(
            formal_name=self.name,
            app_id=self.app_id,
            startup=test_startup_function,
            id=self.id,
        )

    def test_app_name(self):
        self.assertEqual(self.app.name, self.name)

    def test_app_icon(self):
        # App icon will default to a name autodetected from the running module
        self.assertEqual(self.app.icon.path, Path("resources/toga"))
        # This icon will be bound
        self.assertIsNotNone(self.app.icon._impl)

        # Set the icon to a different resource
        self.app.icon = "other.icns"
        self.assertEqual(self.app.icon.path, Path("other.icns"))

        # This icon name will *not* exist. The Impl will be the DEFAULT_ICON's impl
        self.assertEqual(self.app.icon._impl, toga.Icon.DEFAULT_ICON._impl)

    def test_app_app_id(self):
        self.assertEqual(self.app.app_id, self.app_id)

    def test_app_id(self):
        self.assertEqual(self.app.id, self.id)

    def test_widgets_registry(self):
        self.assertTrue(isinstance(self.app.widgets, WidgetRegistry))
        self.assertEqual(len(self.app.widgets), 0)

    def test_app_main_loop_call_impl_main_loop(self):
        self.app.main_loop()
        self.assertActionPerformed(self.app, "main loop")

    def test_app_startup(self):
        self.app.startup()

        self.assertTrue(self.started)
        self.assertEqual(self.app.main_window.content, self.content)
        self.assertEqual(self.app.main_window.app, self.app)
        self.assertActionPerformed(self.app.main_window, "show")

    def test_is_full_screen(self):
        self.assertFalse(self.app.is_full_screen)

        self.app.set_full_screen(self.app.main_window)
        self.assertTrue(self.app.is_full_screen)

        self.app.set_full_screen(["window1", "window2", "window3"])
        self.assertTrue(self.app.is_full_screen)

        self.app.set_full_screen()
        self.assertFalse(self.app.is_full_screen)

    def test_app_exit(self):
        def exit_handler(widget):
            return True

        self.app.on_exit = exit_handler
        self.assertIs(self.app.on_exit._raw, exit_handler)
        self.app.exit()

        self.assertActionPerformed(self.app, "exit")

    def test_full_screen(self):
        # set full screen and exit full screen
        self.app.set_full_screen(self.app.main_window)
        self.assertTrue(self.app.is_full_screen)
        self.app.exit_full_screen()
        self.assertFalse(self.app.is_full_screen)
        # set full screen and set full with no args
        self.app.set_full_screen(self.app.main_window)
        self.assertTrue(self.app.is_full_screen)
        self.app.set_full_screen()
        self.assertFalse(self.app.is_full_screen)

    def test_add_window(self):
        self.assertEqual(len(self.app.windows), 0)
        test_window = toga.Window()
        self.assertEqual(len(self.app.windows), 1)
        self.app.windows += test_window
        self.assertEqual(len(self.app.windows), 1)
        self.assertIs(test_window.app, self.app)

        not_a_window = "not_a_window"
        with self.assertRaises(TypeError):
            self.app.windows += not_a_window

    def test_remove_window(self):
        test_window = toga.Window()
        self.assertEqual(len(self.app.windows), 1)
        self.app.windows -= test_window
        self.assertEqual(len(self.app.windows), 0)

        with self.assertRaises(TypeError):
            self.app.windows -= "not_a_window"

        with self.assertRaises(AttributeError):
            self.app.windows -= test_window

    def test_app_contains_window(self):
        test_window = toga.Window()
        self.assertTrue(test_window in self.app.windows)
        self.app.windows -= test_window
        self.assertFalse(test_window in self.app.windows)

    def test_window_iteration(self):
        test_windows = [
            toga.Window(id=1),
            toga.Window(id=2),
            toga.Window(id=3),
        ]
        for window in test_windows:
            self.app.windows += window
        self.assertEqual(len(self.app.windows), 3)

        for window in self.app.windows:
            self.assertIn(window, test_windows)

    def test_beep(self):
        self.app.beep()
        self.assertActionPerformed(self.app, "beep")

    def test_add_background_task(self):
        thing = Mock()

        async def test_handler(sender):
            thing()

        self.app.add_background_task(test_handler)

        async def run_test():
            # Give the background task time to run.
            await asyncio.sleep(0.1)
            thing.assert_called_once()

        self.app._impl.loop.run_until_complete(run_test())

    def test_override_startup(self):
        class BadApp(toga.App):
            "A startup method that doesn't assign main window raises an error (#760)"

            def startup(self):
                # Override startup but don't create a main window
                pass

        app = BadApp(app_name="bad_app", formal_name="Bad Aoo", app_id="org.beeware")
        with self.assertRaisesRegex(
            ValueError,
            r"Application does not have a main window.",
        ):
            app.main_loop()


class DocumentAppTests(TestCase):
    def setUp(self):
        super().setUp()

        self.name = "Test Document App"
        self.app_id = "beeware.org"
        self.id = "id"

        self.content = Mock()

        self.app = toga.DocumentApp(self.name, self.app_id, id=self.id)

    def test_app_documents(self):
        self.assertEqual(self.app.documents, [])

        doc = Mock()
        self.app._documents.append(doc)
        self.assertEqual(self.app.documents, [doc])

    def test_override_startup(self):
        mock = Mock()

        class DocApp(toga.DocumentApp):
            def startup(self):
                # A document app doesn't have to provide a Main Window.
                mock()

        app = DocApp(app_name="docapp", formal_name="Doc App", app_id="org.beeware")
        app.main_loop()
        mock.assert_called_once()
