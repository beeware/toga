import toga
from colosseum import CSS


class Test{{ cookiecutter.widget_name }}App(toga.App):
    # Button callback functions
    def do_stuff(self, widget, *kwargs):
        self.label.text = "Do stuff."

    def do_clear(self, widget, *kwargs):
        self.label.text = "Ready."

    def startup(self):
      # Label to show responses.
      label = toga.Label('Ready.')

      widget = toga.{{ cookiecutter.widget_name }}()

      # Buttons
      btn_style = CSS(flex=1)
      btn_do_stuff = toga.Button('Do stuff', on_press=self.do_stuff, style=btn_style)
      btn_clear = toga.Button('Clear', on_press=do_clear, style=btn_style)
      btn_box = toga.Box(
          children=[
              btn_do_stuff,
              btn_clear
          ],
          style=CSS(flex_direction='row')
      )

      # Outermost box
      box = toga.Box(
          children=[btn_box, widget, label],
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
    return Test{{ cookiecutter.widget_name }}App('Test {{ cookiecutter.formal_name }}', 'org.pybee.widgets.{{ cookiecutter.name }}')


if __name__ == '__main__':
    app = main()
    app.main_loop()
