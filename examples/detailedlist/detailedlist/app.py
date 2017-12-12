import asyncio

import toga
from colosseum import CSS

from .translations import bee_translations


class ExampleDetailedListApp(toga.App):
    # Detailed list callback functions
    def on_select_handler(self, widget, row, **kwargs):
        self.label.text = 'You selected row: {}'.format(row) if row is not None else 'No row selected'

    async def on_refresh_handler(self, widget, **kwargs):
        self.label.text = 'Refreshing list...'
        # We are using a local data source, so there's literally no reason
        # to use refresh. However, for demonstration purposes, lets pretend
        # that we're getting the data from an API, which takes 1s to respond.
        await asyncio.sleep(1)
        self.label.text = 'List was refreshed.'

    def on_delete_handler(self, widget, row, **kwargs):
        self.label.text = 'Row {} is going to be deleted.'.format(row.subtitle)

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(self.name)
        self.main_window.app = self

        # Label to show responses.
        self.label = toga.Label('Ready.')

        widget = toga.DetailedList(
            data=[
                {
                    'icon': toga.Icon('resources/brutus.png'),
                    'title': translation['string'],
                    'subtitle': translation['country'],
                }
                for translation in bee_translations
            ],
            on_select=self.on_select_handler,
            # on_delete=self.on_delete_handler,
            on_refresh=self.on_refresh_handler,
            style=CSS(flex=1)
        )

        # Outermost box
        outer_box = toga.Box(
            children=[widget, self.label],
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
    return ExampleDetailedListApp('Detailed List', 'org.pybee.widgets.detailedlist')


if __name__ == '__main__':
    app = main()
    app.main_loop()
