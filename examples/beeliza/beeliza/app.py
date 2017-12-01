import asyncio
import random

import toga
from colosseum import CSS

from .bot import Eliza


class BeelizaApp(toga.App):
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
        # Scroll so the most recent entry is visible.
        self.chat.scroll_to_bottom()

        # The partner needs to think about their response...
        await asyncio.sleep(random.random() * 3)

        # ... and they respond
        response = self.partner.respond(input_text)
        # Display the response
        self.chat.data.append(
            icon=toga.Icon('resources/brutus.png'),
            title='Brutus',
            subtitle=response,
        )

        # Scroll so the most recent entry is visible.
        self.chat.scroll_to_bottom()

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)
        self.main_window.app = self

        self.partner = Eliza()

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
        send_button = toga.Button('Send', on_press=self.handle_input, style=CSS(margin_left=10))
        input_box = toga.Box(
            children=[
                self.text_input,
                send_button
            ],
            style=CSS(
                flex_direction='row',
                padding=10,
            )
        )

        # Outermost box
        outer_box = toga.Box(
            children=[self.chat, input_box],
            style=CSS(
                flex=1,
                flex_direction='column'
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return BeelizaApp('Beeliza', 'org.pybee.beeliza')


if __name__ == '__main__':
    app = main()
    app.main_loop()
