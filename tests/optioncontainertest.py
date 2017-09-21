import toga
from colosseum import CSS

from src.winforms.toga_winforms.widgets.optioncontainer import OptionContainer


class OptionContainerTest(toga.App):
    def calculate(self, widget):
        try:
            self.c_input.value = (float(self.f_input.value) - 32.0) * 5.0 / 9.0
        except Exception:
            self.c_input.value = '???'

    def get_container(self, container, contents):

        for item in contents:
            container.add(str(item), item)

        return container

    def startup(self):
        self.main_window = toga.MainWindow(self.name)
        self.main_window.app = self

        # Tutorial 1
        c_box = toga.Box()
        f_box = toga.Box()
        box = toga.Box()

        self.c_input = toga.TextInput(readonly=True)
        self.f_input = toga.TextInput()

        c_label = toga.Label('Celcius', alignment=toga.LEFT_ALIGNED)
        f_label = toga.Label('Fahrenheit', alignment=toga.LEFT_ALIGNED)
        join_label = toga.Label('is equivalent to', alignment=toga.RIGHT_ALIGNED)

        button = toga.Button('Calculate', on_press=self.calculate)
        container = OptionContainer(style=CSS(width=600))

        f_box.add(self.f_input)
        f_box.add(f_label)

        c_box.add(join_label)
        c_box.add(self.c_input)
        c_box.add(c_label)

        box.add(f_box)
        box.add(c_box)
        box.add(button)

        table = toga.Table(['Hello', 'World'])


        t_box = toga.Box(style=CSS(width=500, height=300, padding_top=50, flex_direction='row'))
        t_box.add(toga.TextInput(style=CSS(width=400)))
        t_box.add(toga.Button("Hi"))
        table.insert(None, 'Value 1', 'Value 2')

        container = self.get_container(container, [box, table, t_box])

        container.add("test", toga.TextInput(style=CSS(width=400)))

        box.style.set(flex_direction='column', padding_top=10)

        x_box = toga.Box(style=CSS(flex_direction="column"))
        x_box.add(t_box)
        self.main_window.content = container
        self.main_window.show()


def main():
    return OptionContainerTest('Converter', 'org.pybee.converter')


if __name__ == '__main__':
    main().main_loop()
