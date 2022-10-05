import time
import unittest

import toga
from toga.style import Pack
import pyautogui

from threading import Thread


class ButtonApp(toga.App):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.started = False
        self.clicked = False

    def on_click(self, widget):
        self.clicked = True

    def startup(self):
        # Window class
        #   Main window of the application with title and size
        #   Also make the window non-resizable and non-minimizable.
        self.main_window = toga.MainWindow(
            title=self.name, size=(800, 500),
            resizeable=False, minimizable=False
        )

        # Button class
        #   Simple button with text and callback function called when
        #   hit the button
        self.button1 = toga.Button(
            'Change Text',
            style=Pack(flex=1),
            id="button1",
            on_press=self.on_click
        )

        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[
                self.button1
            ]
        )

        # Show the main window
        self.main_window.show()
        self.started = True


class TestButtonUi(unittest.TestCase):

    def setUp(self):
        self.app = ButtonApp('Button', 'org.beeware.ui_test.button')
        self.thread = Thread(
            target=self.app.main_loop, kwargs=dict(handle_sigint=False)
        )
        self.thread.start()
        time.sleep(0.5)

    def tearDown(self):
        self.app.exit()
        time.sleep(0.5)

    def test_button_click_with_on_click(self):
        cx, cy = self.app.main_window.content_position
        bx, by = (
            self.app.button1.layout.absolute_content_top,
            self.app.button1.layout.absolute_content_left,
        )
        w, h = (
            self.app.button1.layout.content_width,
            self.app.button1.layout.content_height,
        )
        self.assertFalse(self.app.clicked)
        pyautogui.moveTo(cx + bx + w // 2, cy + by + h // 2)
        pyautogui.click()
        self.assertTrue(self.app.clicked)

    def test_button_click_when_disabled(self):
        self.app.button1.enabled = False
        cx, cy = self.app.main_window.content_position
        bx, by = (
            self.app.button1.layout.absolute_content_top,
            self.app.button1.layout.absolute_content_left,
        )
        w, h = (
            self.app.button1.layout.content_width,
            self.app.button1.layout.content_height,
        )
        self.assertFalse(self.app.clicked)
        pyautogui.moveTo(cx + bx + w // 2, cy + by + h // 2)
        pyautogui.click()
        self.assertFalse(self.app.clicked)

    def test_button_color(self):
        self.app.button1.style.background_color = "green"
        time.sleep(0.1)
        cx, cy = self.app.main_window.content_position
        bx, by = (
            self.app.button1.layout.absolute_content_top,
            self.app.button1.layout.absolute_content_left,
        )
        w, h = (
            self.app.button1.layout.content_width,
            self.app.button1.layout.content_height,
        )
        pixel = pyautogui.pixel(cx + bx + w // 3, cy + by + h // 3)
        self.assertEqual(
            pixel, (0, 128, 0)
        )
