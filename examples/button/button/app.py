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

        inner_box1 = toga.Box(
            style=style_inner_box,
            children=[
                button1,
                self.button2,
                button3,
            ]
        )

        # Button with label and callback function called
        button4a = toga.Button('Make window larger', on_press=self.callbackLarger)
        button4b = toga.Button('Make window smaller', on_press=self.callbackSmaller)

        # Add components for the second row of the outer box
        inner_box2 = toga.Box(
            style=style_inner_box,
            children=[
                button4a,
                button4b,
            ]
        )

        # Button with label and margin style
        button5 = toga.Button('Far from home', style=Pack(padding=50, color=BLUE))

        # Button with label and RGB color
        button6 = toga.Button('RGB : Fashion', style=Pack(padding=10, background_color=RED))

        # Button with label and string color
        button7 = toga.Button('String : Fashion', style=Pack(padding=10, background_color=BLUE))

        # Button with label and string color
        button8 = toga.Button('Big Font', style=Pack(padding=5, font_family='serif', font_size=20, font_weight='bold'))

        # Add components for the third row of the outer box
        inner_box3 = toga.Box(
            style=style_inner_box,
            children=[
                button5,
                button6,
                button7,
                button8,
            ]
        )

        # Buttons to change window position
        button9 = toga.Button('Not quite the origin', style=Pack(padding=5), on_press=self.seek_origin)
        button10 = toga.Button('To the left screen', style=Pack(padding=5), on_press=self.seek_left_screen)
        button11 = toga.Button('To the right screen', style=Pack(padding=5), on_press=self.seek_right_screen)
        button12 = toga.Button('Bump left', style=Pack(padding=5), on_press=self.bump_left)
        button13 = toga.Button('Bump right', style=Pack(padding=5), on_press=self.bump_right)

        # Add components for the fourth row of the outer box
        inner_box4 = toga.Box(
            style=style_inner_box,
            children=[
                button9,
                button10,
                button11,
                button12,
                button13,
            ]
        )

        #  Create the outer box with 4 rows
        outer_box = toga.Box(
            style=Pack(direction=COLUMN, height=10),
            children=[inner_box1, inner_box2, inner_box3, inner_box4]
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

    def seek_origin(self, button):
        # Move the window to the somewhere near the top-left of the main screen
        self.main_window.position = (100, 30)

    def seek_right_screen(self, button):
        # Move the window off the right hand side of the main screen.
        # If the user has multiple monitors with a screen to the right
        # of the main screen, the window should appear there.
        self.main_window.position = (2000, 400)

    def seek_left_screen(self, button):
        # Move the window off the left hand side of the main screen.
        # If the user has multiple monitors with a screen to the left
        # of the main screen, the window should appear there.
        self.main_window.position = (-1000, 300)

    def bump_left(self, button):
        # Move the window to the left a bit.
        x, y = self.main_window.position
        self.main_window.position = (x - 50, y)

    def bump_right(self, button):
        # Move the window to the right a bit.
        x, y = self.main_window.position
        self.main_window.position = (x + 50, y)


def main():
    # Application class
    #   App name and namespace
    app = ExampleButtonApp('Button', 'org.beeware.widgets.buttons')
    return app


if __name__ == '__main__':
    app = main()
    app.main_loop()
