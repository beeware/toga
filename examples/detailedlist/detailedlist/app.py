import asyncio

import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack

from .translations import bee_translations


class ExampleDetailedListApp(toga.App):
    # Detailed list callback functions
    def on_select_handler(self, widget, row, **kwargs):
        self.label.text = 'Bee is {} in {}'.format(row.title, row.subtitle) \
            if row is not None else 'No row selected'
        # TODO: remove self.selected_row when #962 is implemented
        self.selected_row = row

    async def on_refresh_handler(self, widget, **kwargs):
        self.label.text = 'Refreshing list...'
        # We are using a local data source, so there's literally no reason
        # to use refresh. However, for demonstration purposes, lets pretend
        # that we're getting the data from an API, which takes 1s to respond.
        await asyncio.sleep(1)
        self.label.text = 'List was refreshed.'

    def on_delete_handler(self, widget, row, **kwargs):
        self.label.text = 'Row {} is going to be deleted.'.format(row.subtitle)
        self.selected_row = None

    # Button callback functions
    def insert_handler(self, widget, **kwargs):
        item = {"icon": None, "subtitle": "The Hive", "title": "Bzzz!"}
        if self.selected_row:
            self.dl.data.insert(self.dl.data.index(self.selected_row) + 1, **item)
        else:
            self.dl.data.append(**item)
        self.dl.scroll_to_row(len(self.dl.data) - 1)

    def remove_handler(self, widget, **kwargs):
        selection = self.selected_row
        if selection:
            self.dl.data.remove(selection)

    def startup(self):
        self.selected_row = None

        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Buttons
        btn_style = Pack(flex=1, padding=10)
        self.btn_insert = toga.Button('Insert Row', on_press=self.insert_handler, style=btn_style)
        self.btn_remove = toga.Button('Remove Row', on_press=self.remove_handler, style=btn_style)
        self.btn_box = toga.Box(children=[self.btn_insert, self.btn_remove], style=Pack(direction=ROW))

        # Label to show responses.
        self.label = toga.Label('Ready.')

        self.dl = toga.DetailedList(
            data=[
                {
                    'icon': toga.Icon('resources/brutus.png'),
                    'title': translation['string'],
                    'subtitle': translation['country'],
                }
                for translation in bee_translations
            ],
            on_select=self.on_select_handler,
            on_delete=self.on_delete_handler,
            on_refresh=self.on_refresh_handler,
            style=Pack(flex=1)
        )

        # Outermost box
        outer_box = toga.Box(
            children=[self.btn_box, self.dl, self.label],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleDetailedListApp('Detailed List', 'org.beeware.widgets.detailedlist')


if __name__ == '__main__':
    app = main()
    app.main_loop()
