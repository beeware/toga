from string import ascii_lowercase, ascii_uppercase, digits

import toga
from toga import validators
from toga.constants import COLUMN
from toga.style import Pack

EMPTY_PASSWORD = "Empty password"


class PasswordInputApp(toga.App):
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
        return "Password contains: {}".format(", ".join(contains))

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)
        PADDING = 5
        # Label to show responses.
        self.label = toga.Label("Testing Password")
        self.password_content_label = toga.Label(
            EMPTY_PASSWORD, style=Pack(padding_bottom=PADDING)
        )

        # Padding box only
        self.password_input = toga.PasswordInput(
            placeholder="Password...",
            style=Pack(padding=PADDING),
            on_change=self.on_password_change,
            validators=[
                validators.MinLength(10),
                validators.ContainsUppercase(),
                validators.ContainsLowercase(),
                validators.ContainsSpecial(),
                validators.ContainsDigit(),
            ],
        )

        # Outermost box
        children = [
            self.label,
            self.password_input,
            self.password_content_label,
        ]
        outer_box = toga.Box(
            children=children,
            style=Pack(flex=1, direction=COLUMN, padding=10, width=500, height=300),
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return PasswordInputApp("PasswordInput", "org.beeware.widgets.passwordinput")


if __name__ == "__main__":
    app = main()
    app.main_loop()
