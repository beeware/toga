import toga


def button_handler(widget):
    print("hello")
    widget.style.color = "green"

def button_handler2(widget):
    print("hello")
    del button.style.color

def build(app):
    box = toga.Box()

    global button
    button = toga.Button("Hello world", on_press=button_handler)
    button2 = toga.Button("Hello world", on_press=button_handler2)
    button2.style.padding = 50
    button.style.padding = 50
    button.style.flex = 1
    box.add(button)
    box.add(button2)

    return box


def main():
    return toga.App("First App", "org.beeware.helloworld", startup=build)


if __name__ == "__main__":
    main().main_loop()
