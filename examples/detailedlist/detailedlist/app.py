import toga
from colosseum import CSS

from .translations import bee_translations


class TestDetailedListApp(toga.App):
    # Detailed list callback functions
    def on_select(widget, row, **kwargs):
        self.label.text('Row {} was selected.'.format(row))

    def on_refresh(widget, **kwargs):
        self.label.text('List was refreshed.')

    def on_delete(widget, row, **kwargs):
        self.label.text('Row {} is going to be deleted.'.format(row))

    def startup(self):
      # Label to show responses.
      label = toga.Label('Ready.')

      widget = toga.DetailedList(
          data=[
              '{country}: {string}'.format(**translation)
              for translation in bee_translations
          ],
          on_select=on_select,
          on_delete=on_delete,
          on_refresh=on_refresh,
      )

      # Outermost box
      box = toga.Box(
          children=[widget, label],
          style=CSS(
              flex=1,
              flex_direction='column',
              padding=10,
              min_width=500,
              min_height=300
          )
      )
      return box


def main():
    return TestDetailedListApp('Test Detailed List', 'org.pybee.widgets.detailedlist')


if __name__ == '__main__':
    app = main()
    app.main_loop()
