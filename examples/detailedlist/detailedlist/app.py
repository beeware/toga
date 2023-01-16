import asyncio

import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack

from .translations import bee_translations


class ExampleDetailedListApp(toga.App):
    # Detailed list callback functions
    def on_select_handler(self, widget, row, **kwargs):
        self.label.text = (
            f"Bee is {row.title} in {row.subtitle}"
            if row is not None
            else "No row selected"
        )

    async def on_refresh_handler(self, widget, **kwargs):
        self.label.text = "Refreshing list..."
        # We are using a local data source, so there's literally no reason
        # to use refresh. However, for demonstration purposes, lets pretend
        # that we're getting the data from an API, which takes 1s to respond.
        await asyncio.sleep(1)
        self.label.text = "List was refreshed."

    def on_delete_handler(self, widget, row, **kwargs):
        self.label.text = f"Row {row.subtitle} is going to be deleted."

    # Button callback functions
    def insert_handler(self, widget, **kwargs):
        item = {"icon": None, "subtitle": "The Hive", "title": "Bzzz!"}
        if self.dl.selection:
            index = self.dl.data.index(self.dl.selection) + 1
            self.dl.data.insert(index, **item)
        else:
            index = len(self.dl.data)
            self.dl.data.append(**item)
        self.dl.scroll_to_row(index)

    def remove_handler(self, widget, **kwargs):
        if self.dl.selection:
            self.dl.data.remove(self.dl.selection)

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Buttons
        btn_style = Pack(flex=1, padding=10)
        self.btn_insert = toga.Button(
            "Insert Row", on_press=self.insert_handler, style=btn_style
        )
        self.btn_remove = toga.Button(
            "Remove Row", on_press=self.remove_handler, style=btn_style
        )
        self.btn_box = toga.Box(
            children=[self.btn_insert, self.btn_remove], style=Pack(direction=ROW)
        )

        # Label to show responses.
        self.label = toga.Label("Ready.")

        self.dl = toga.DetailedList(
            data=[
                {
                    "icon": toga.Icon("resources/brutus.png"),
                    "title": translation["string"],
                    "subtitle": translation["country"],
                }
                for translation in bee_translations
            ],
            on_select=self.on_select_handler,
            on_delete=self.on_delete_handler,
            on_refresh=self.on_refresh_handler,
            style=Pack(flex=1),
        )

        # Outermost box
        outer_box = toga.Box(
            children=[self.btn_box, self.dl, self.label],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
            ),
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleDetailedListApp("Detailed List", "org.beeware.widgets.detailedlist")


if __name__ == "__main__":
    app = main()
    app.main_loop()
