from string import ascii_lowercase, ascii_uppercase, digits

import toga
from toga.constants import COLUMN
from toga.style import Pack

EMPTY_PASSWORD = 'Empty password'


class TextInputApp(toga.App):
    # Button callback functions
    def do_extract_values(self, widget, **kwargs):
        # Disable all the text inputs
        self.text_input.enabled = False
        self.password_input.enabled = False
        self.number_input.enabled = False

        # Update the labels with the extracted values
        self.text_label.text = "Text content: {}".format(
            self.text_input.value
        )

        self.password_label.text = "Your password is: {}".format(
            self.password_input.value
        )

        number = self.number_input.value
        if number:
            self.number_label.text = "Double the number is: {}".format(number * 2)
        else:
            self.number_label.text = "You didn't enter a number"

        # Wait 5 seconds
        self.label.text = 'Counting down from 5...'
        yield 1
        self.label.text = 'Counting down from 4...'
        yield 1
        self.label.text = 'Counting down from 3...'
        yield 1
        self.label.text = 'Counting down from 2...'
        yield 1
        self.label.text = 'Counting down from 1...'
        yield 1
        self.label.text = 'Enter some values and press extract.'

        # Renable the inputs again.
        self.text_input.enabled = True
        self.password_input.enabled = True
        self.number_input.enabled = True

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Labels to show responses.
        self.label = toga.Label(
            'Enter some values and press extract.', style=Pack(padding=10)
        )
        self.text_label = toga.Label('Ready.', style=Pack(padding=10))
        self.password_label = toga.Label('Ready.', style=Pack(padding=10))
        self.password_content_label = toga.Label(
            EMPTY_PASSWORD, style=Pack(padding_bottom=10, font_size=9)
        )
        self.number_label = toga.Label('Ready.', style=Pack(padding=10))

        # Text inputs and a button
        self.text_input = toga.TextInput(
            placeholder='Type something...', style=Pack(padding=10)
        )
        self.password_input = toga.PasswordInput(
            placeholder='Password...',
            style=Pack(padding=10),
            on_change=self.on_password_change
        )
        self.number_input = toga.NumberInput(style=Pack(padding=10))
        btn_extract = toga.Button(
            'Extract values',
            on_press=self.do_extract_values,
            style=Pack(flex=1)
        )

        # Outermost box
        box = toga.Box(
            children=[
                self.label,
                self.text_input,
                self.password_input,
                self.password_content_label,
                self.number_input,
                self.text_label,
                self.password_label,
                self.number_label,
                btn_extract,
            ],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
            )
        )

        # Add the content on the main window
        self.main_window.content = box

        # Show the main window
        self.main_window.show()

    def on_password_change(self, widget):
        content = widget.value
        self.password_content_label.text = self.get_password_content_label(content)

    def get_password_content_label(self, content):
        if content.strip() == "":
            return EMPTY_PASSWORD
        contains = set()
        for letter in content:
            if letter in ascii_uppercase:
                contains.add("uppercase letters")
            elif letter in ascii_lowercase:
                contains.add("lowercase letters")
            elif letter in digits:
                contains.add("digits")
            else:
                contains.add("special characters")
        return "Password contains: {}".format(', '.join(contains))


def main():
    return TextInputApp('TextInput', 'org.beeware.widgets.textinput')


if __name__ == '__main__':
    app = main()
    app.main_loop()
