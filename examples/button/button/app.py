import random

import toga
from toga.colors import BLUE, RED
from toga.constants import COLUMN, ROW
from toga.style import Pack


class ExampleButtonApp(toga.App):
    def startup(self):
        # Window class
        #   Main window of the application with title and size
        #   Also make the window non-resizable and non-minimizable.
        self.main_window = toga.MainWindow(
            title=self.name, size=(800, 500),
            resizeable=False, minimizable=False
        )

        # Common style of the inner boxes
        style_inner_box = Pack(direction=ROW)

        # Button class
        #   Simple button with label and callback function called when
        #   hit the button
        button1 = toga.Button(
            'Change Label',
            on_press=self.callbackLabel,
            style=Pack(flex=1),
        )

        # Button with label and enable option
        # Keep a reference to it so it can be enabled by another button.
        self.button2 = toga.Button(
            'Button is disabled!',
            enabled=False,
            style=Pack(flex=1),
            on_press=self.callbackDisable,
        )

        # Button with label and style option
        button3 = toga.Button('Bigger', style=Pack(width=200))

        # Button with label and callback function called
        button4a = toga.Button('Make window larger', on_press=self.callbackLarger)
        button4b = toga.Button('Make window smaller', on_press=self.callbackSmaller)

        # Box class
        # Container of components
        #   Add components for the first row of the outer box
        inner_box1 = toga.Box(
            style=style_inner_box,
            children=[
                button1,
                self.button2,
                button3,
                button4a,
                button4b,
            ]
        )

        # Button with label and margin style
        button5 = toga.Button('Far from home', style=Pack(padding=50))

        # Button with label and RGB color
        button6 = toga.Button('RGB : Fashion', style=Pack(background_color=RED))

        # Button with label and string color
        button7 = toga.Button('String : Fashion', style=Pack(background_color=BLUE))

        # Add components for the second row of the outer box
        inner_box2 = toga.Box(
            style=style_inner_box,
            children=[
                button5,
                button6,
                button7
            ]
        )

        #  Create the outer box with 2 rows
        outer_box = toga.Box(
            style=Pack(direction=COLUMN, height=10),
            children=[inner_box1, inner_box2]
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()

    def callbackLabel(self, button):
        # Some action when you hit the button
        #   In this case the label will change
        button.label = 'Magic {val}!!'.format(val=random.randint(0, 100))

        # If the disabled button isn't enabled, enable it.
        if not self.button2.enabled:
            self.button2.enabled = True
            self.button2.label = 'Disable button'

    def callbackDisable(self, button):
        button.enabled = False
        button.label = 'Button is disabled!'

    def callbackLarger(self, button):
        # Some action when you hit the button
        #   In this case the window size will change
        self.main_window.size = (1000, 600)

    def callbackSmaller(self, button):
        # Some action when you hit the button
        #   In this case the window size will change
        self.main_window.size = (200, 200)


def main():
    # Application class
    #   App name and namespace
    app = ExampleButtonApp('Button', 'org.beeware.widgets.buttons')
    return app
