import toga


def build(app):
    c_box = toga.Box()
    f_box = toga.Box()
    box = toga.Box()

    c_input = toga.TextInput(readonly=True)
    f_input = toga.TextInput()

    c_label = toga.Label('Celsius', alignment=toga.LEFT_ALIGNED)
    f_label = toga.Label('Fahrenheit', alignment=toga.LEFT_ALIGNED)
    join_label = toga.Label('is equivalent to', alignment=toga.RIGHT_ALIGNED)

    def calculate(widget):
        try:
            c_input.value = (float(f_input.value) - 32.0) * 5.0 / 9.0
        except:
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

    box.style.set(flex_direction='column', padding_top=10)
    f_box.style.set(flex_direction='row', margin=5)
    c_box.style.set(flex_direction='row', margin=5)

    c_input.style.set(flex=1)
    f_input.style.set(flex=1, margin_left=160)
    c_label.style.set(width=100, margin_left=10)
    f_label.style.set(width=100, margin_left=10)
    join_label.style.set(width=150, margin_right=10)

    button.style.set(margin=15)

    return box


def main():
    return toga.App('Temperature Converter', 'org.pybee.f_to_c', startup=build)
