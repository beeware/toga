import asyncio
import random

import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack

from .bot import Eliza


class BeelizaApp(toga.App):
    async def handle_input(self, widget, **kwargs):
        # Display the input as a chat entry.
        input_text = self.text_input.value
        self.chat.data.append(
            # User's avatar is from http://avatars.adorable.io
            # using user@beeware.org
            icon=toga.Icon("resources/user.png"),
            title="You",
            subtitle=input_text,
        )
        # Clear the current input, ready for more input.
        self.text_input.value = ""
        # Scroll so the most recent entry is visible.
        self.chat.scroll_to_bottom()

        # The partner needs to think about their response...
        await asyncio.sleep(random.random() * 3)

        # ... and they respond
        response = self.partner.respond(input_text)
        # Display the response
        self.chat.data.append(
            icon=toga.Icon("resources/brutus.png"),
            title="Brutus",
            subtitle=response,
        )

        # Scroll so the most recent entry is visible.
        self.chat.scroll_to_bottom()

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        self.partner = Eliza()

        self.chat = toga.DetailedList(
            data=[
                {
                    "icon": toga.Icon("resources/brutus.png"),
                    "title": "Brutus",
                    "subtitle": "Hello. How are you feeling today?",
                }
            ],
            style=Pack(flex=1),
        )

        # Buttons
        self.text_input = toga.TextInput(style=Pack(flex=1, padding=5))
        send_button = toga.Button(
            "Send", on_press=self.handle_input, style=Pack(padding=5)
        )
        input_box = toga.Box(
            children=[self.text_input, send_button], style=Pack(direction=ROW)
        )

        # Outermost box
        outer_box = toga.Box(
            children=[self.chat, input_box], style=Pack(direction=COLUMN)
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return BeelizaApp("Beeliza", "org.beeware.beeliza")


if __name__ == "__main__":
    app = main()
    app.main_loop()
