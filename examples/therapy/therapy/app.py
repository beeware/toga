import asyncio
import random

import toga
from colosseum import CSS

from .therapist import Eliza


class TherapyApp(toga.App):
    async def handle_input(self, widget, **kwargs):
        # Display the input as a chat entry.
        input_text = self.text_input.value
        self.chat.data.append(
            # User's avatar is from http://avatars.adorable.io
            # using user@beeware.org
            icon=toga.Icon('resources/user.png'),
            title='You',
            subtitle=input_text,
        )
        # Clear the current input, ready for more input.
        self.text_input.value = ''

        # The therapist needs to think about their response...
        await asyncio.sleep(random.random() * 3)

        # ... and they respond
        response = self.therapist.respond(input_text)
        # Display the response
        self.chat.data.append(
            icon=toga.Icon('resources/brutus.png'),
            title='Brutus',
            subtitle=response,
        )

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(self.name)
        self.main_window.app = self

        self.therapist = Eliza()

        self.chat = toga.DetailedList(
            data=[
                {
                    'icon': toga.Icon('resources/brutus.png'),
                    'title': 'Brutus',
                    'subtitle': 'Hello. How are you feeling today?',
                }
            ],
            style=CSS(flex=1)
        )

        # Buttons
        self.text_input = toga.TextInput(style=CSS(flex=1))
        send_button = toga.Button('Send', on_press=self.handle_input)
        input_box = toga.Box(
            children=[
                self.text_input,
                send_button
            ],
            style=CSS(flex_direction='row')
        )

        # Outermost box
        outer_box = toga.Box(
            children=[self.chat, input_box],
            style=CSS(
                flex=1,
                flex_direction='column',
                padding=10,
                min_width=500,
                min_height=300
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return TherapyApp('Therapy', 'org.pybee.therapy')


if __name__ == '__main__':
    app = main()
    app.main_loop()
