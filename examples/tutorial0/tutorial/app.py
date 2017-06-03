import toga


def button_handler(widget):
    print("hello")


def build(app):
    box = toga.Box()

    button = toga.Button('Hello world', on_press=button_handler)
    button.style.set(margin=50)
    box.add(button)

    return box


def main():
    return toga.App('First App', 'org.pybee.helloworld', startup=build)
