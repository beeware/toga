import toga
from toga.style.pack import COLUMN, LEFT, RIGHT, ROW, Pack


def build(app):
    c_box = toga.Box()
    f_box = toga.Box()
    box = toga.Box()

    c_input = toga.TextInput(readonly=True)
    f_input = toga.TextInput()

    c_label = toga.Label('Celsius', style=Pack(text_align=LEFT))
    f_label = toga.Label('Fahrenheit', style=Pack(text_align=LEFT))
    join_label = toga.Label('is equivalent to', style=Pack(text_align=RIGHT))

    def calculate(widget):
        try:
            c_input.value = (float(f_input.value) - 32.0) * 5.0 / 9.0
        except ValueError:
            c_input.value = '???'

    button = toga.Button('Calculate', on_press=calculate)

    f_box.add(f_input)
    f_box.add(f_label)

    c_box.add(join_label)
    c_box.add(c_input)
    c_box.add(c_label)

    box.add(f_box)
    box.add(c_box)
    box.add(button)

    box.style.update(direction=COLUMN, padding_top=10)
    f_box.style.update(direction=ROW, padding=5)
    c_box.style.update(direction=ROW, padding=5)

    c_input.style.update(flex=1)
    f_input.style.update(flex=1, padding_left=160)
    c_label.style.update(width=100, padding_left=10)
    f_label.style.update(width=100, padding_left=10)
    join_label.style.update(width=150, padding_right=10)

    button.style.update(padding=15, flex=1)

    return box


def main():
    return toga.App('Temperature Converter', 'org.beeware.f_to_c', startup=build)


if __name__ == '__main__':
    main().main_loop()
