import asyncio
from string import ascii_lowercase, ascii_uppercase, digits

import toga
from toga import validators
from toga.constants import COLUMN, RIGHT

EMPTY_PASSWORD = "Empty password"


class TextInputApp(toga.App):
    # Button callback functions
    async def do_extract_values(self, widget, **kwargs):
        # Disable all the text inputs
        for input in self.inputs:
            input.enabled = False

        # Update the labels with the extracted values
        self.text_label.text = (
            "Text content: "
            f"{self.text_input.value}; {self.text_input_placeholder.value}"
        )

        self.password_label.text = "Your password is {}: {}".format(
            "valid" if self.password_input.is_valid else "invalid",
            self.password_input.value,
        )

        try:
            number = self.number_input.value + self.right_aligned_number_input.value
            self.number_label.text = (
                f"The sum of {self.number_input.value} and "
                f"{self.right_aligned_number_input.value} is {number}."
            )
        except TypeError:
            self.number_label.text = "Please enter a number in each number input."

        # Wait a few seconds
        for i in range(2, 0, -1):
            self.label.text = f"Counting down from {i}..."
            await asyncio.sleep(1)
        self.label.text = "Enter some values and press extract."

        # Re-enable the inputs again.
        for input in self.inputs:
            input.enabled = True

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow()
        PADDING = 5

        # Labels to show responses.
        self.label = toga.Label("Enter some values and press extract.", margin=PADDING)
        self.text_label = toga.Label("Ready.", margin=PADDING)
        self.password_label = toga.Label("Ready.", margin=PADDING)
        self.password_content_label = toga.Label(
            EMPTY_PASSWORD, margin_bottom=PADDING, font_size=9
        )
        self.number_label = toga.Label("Ready.", margin=PADDING)

        # Text inputs and a button
        self.text_input = toga.TextInput(
            value="Initial value, and on_confirm handler",
            placeholder="Type something...",
            margin=PADDING,
            on_confirm=self.do_extract_values,
        )
        self.right_aligned_input = toga.TextInput(
            placeholder="Right aligned text",
            margin=PADDING,
            text_align=RIGHT,
        )
        self.text_input_placeholder = toga.TextInput(
            placeholder="Type something...", margin=PADDING
        )
        self.password_input = toga.PasswordInput(
            placeholder="Password...",
            margin=PADDING,
            on_change=self.on_password_change,
            validators=[
                validators.MinLength(10),
                validators.ContainsUppercase(),
                validators.ContainsLowercase(),
                validators.ContainsSpecial(),
                validators.ContainsDigit(),
            ],
        )
        self.email_input = toga.TextInput(
            placeholder="Email...",
            margin=PADDING,
            validators=[validators.Email()],
        )
        self.number_input = toga.NumberInput(margin=PADDING)
        btn_extract = toga.Button(
            "Extract values",
            on_press=self.do_extract_values,
            flex=1,
        )
        self.right_aligned_number_input = toga.NumberInput(
            margin=PADDING, text_align=RIGHT
        )

        children = [
            self.label,
            self.text_input,
            self.right_aligned_input,
            self.text_input_placeholder,
            self.password_input,
            self.password_content_label,
            self.email_input,
            self.number_input,
            self.right_aligned_number_input,
            self.text_label,
            self.password_label,
            self.number_label,
            btn_extract,
        ]
        self.inputs = [
            child
            for child in children
            if isinstance(child, (toga.TextInput, toga.NumberInput))
        ]

        # Outermost box
        box = toga.Box(
            children=children,
            flex=1,
            direction=COLUMN,
            margin=PADDING,
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
        return "Password contains: {}".format(", ".join(contains))


def main():
    return TextInputApp("TextInput", "org.beeware.toga.examples.textinput")


if __name__ == "__main__":
    main().main_loop()
