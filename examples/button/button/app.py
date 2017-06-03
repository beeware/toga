import toga
from colosseum import CSS, COLUMN, ROW


class StartApp(toga.App):
    def startup(self):
        # Window class
        #   Main window of the application with title and size
        self.main_window = toga.MainWindow(self.name, size=(200, 200))
        self.main_window.app = self

        # Common style of the inner boxes
        style_inner_box = CSS(flex_direction=ROW)

        # Button class
        #   Simple button with label and callback function called when
        #   hit the button
        button1 = toga.Button('Change Label', on_press=self.callbackLabel)

        # Button with label and enable option
        button2 = toga.Button('Disabled', enabled=False)

        # Button with label and style option
        button3 = toga.Button('Bigger', style=CSS(width=200))

        # Button with label and callback function called when
        #   hit the button
        button4 = toga.Button('Resize Window', on_press=self.callbackResize)

        # Box class
        # Container of components
        #   Add components for the first row of the outer box
        inner_box1 = toga.Box(style=style_inner_box,
                            children=[button1,
                                    button2,
                                    button3,
                                    button4])

        # Button with label and margin style
        button5 = toga.Button('Far from home', style=CSS(margin=50))

        # Button with label and RGB color
        button6 = toga.Button('RGB : Fashion', background_color=(50,200,200))

        # Button with label and string color
        button7 = toga.Button('String : Fashion', background_color='yellow')

        # Add components for the second row of the outer box
        inner_box2 = toga.Box(style=style_inner_box,
                            children=[button5,
                                    button6,
                                    button7])

        #  Create the outer box with 2 rows
        outer_box = toga.Box(style=CSS(flex_direction=COLUMN,
                                        height=10),
                            children=[inner_box1, inner_box2])

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()

    def callbackLabel(self, button):
        # Some action when you hit the button
        #   In this case the label will change
        button.label = 'Magic!!'

    def callbackResize(self, button):
        # Some action when you hit the button
        #   In this case the window size will change
        self.main_window.size = (100,100)


def main():
    # Application class
    #   App name and namespace
    app = StartApp('Buttons', 'org.pybee.helloworld')
    return app
