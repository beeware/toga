import toga
from src.winforms.toga_winforms.widgets.optioncontainer import OptionContainer


class OpenContainerTest(toga.App):
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

        widths = []
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
        container = OptionContainer()
        widths.append(container._impl.Width)
        self.main_window.content = container
        widths.append(container._impl.Width)

        f_box.add(self.f_input)
        f_box.add(f_label)

        c_box.add(join_label)
        c_box.add(self.c_input)
        c_box.add(c_label)
        # c_box.add(table)
        box.add(f_box)
        box.add(c_box)
        box.add(button)

        table = toga.Table(['Hello', 'World'])
        table1 = toga.Table(['Heading 1', 'Heading 2'])
        table.insert(None, 'Value 1', 'Value 2')

        widths.append(c_label._impl.Width)
        container = self.get_container(container, [box, table, table1])
        widths.append(c_label._impl.Width)

        box.style.set(flex_direction='column', padding_top=10)

        self.main_window.show()
        print(widths)

        with open("widths.csv", mode="w") as f:
            f.write(",".join(map(str, widths)))

def main():
    return OpenContainerTest('Converter', 'org.pybee.converter')


if __name__ == '__main__':
    main().main_loop()
