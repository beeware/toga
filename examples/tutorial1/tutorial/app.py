import toga
from toga.constants import COLUMN, LEFT, RIGHT, ROW


def build(app):
    c_box = toga.Box()
    f_box = toga.Box()
    box = toga.Box()

    c_input = toga.TextInput(readonly=True)
    f_input = toga.TextInput()

    c_label = toga.Label("Celsius", text_align=LEFT)
    f_label = toga.Label("Fahrenheit", text_align=LEFT)
    join_label = toga.Label("is equivalent to", text_align=RIGHT)

    def calculate(widget):
        try:
            c_input.value = (float(f_input.value) - 32.0) * 5.0 / 9.0
        except ValueError:
            c_input.value = "???"

    button = toga.Button("Calculate", on_press=calculate)

    f_box.add(f_input)
    f_box.add(f_label)

    c_box.add(join_label)
    c_box.add(c_input)
    c_box.add(c_label)

    box.add(f_box)
    box.add(c_box)
    box.add(button)

    box.style.update(direction=COLUMN, margin=10, gap=10)
    f_box.style.update(direction=ROW, gap=10)
    c_box.style.update(direction=ROW, gap=10)

    c_input.style.update(flex=1)
    f_input.style.update(flex=1, margin_left=210)
    c_label.style.update(width=100)
    f_label.style.update(width=100)
    join_label.style.update(width=200)

    button.style.update(margin_top=5)

    return box


def main():
    return toga.App(
        "Temperature Converter",
        "org.beeware.toga.examples.tutorial",
        startup=build,
    )


if __name__ == "__main__":
    main().main_loop()
