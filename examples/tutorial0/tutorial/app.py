import toga
from tutorial import __version__


def button_handler(widget):
    print("hello")


def build(app):
    box = toga.Box()

    button = toga.Button('Hello world', on_press=button_handler)
    button.style.padding = 50
    button.style.flex = 1
    box.add(button)

    return box


def main():
    return toga.App(
        'First App',
        app_id='org.beeware.helloworld',
        author='Tiberius Yak',
        version=__version__,
        startup=build,
    )


if __name__ == '__main__':
    main().main_loop()
