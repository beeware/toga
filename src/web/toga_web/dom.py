
_handlers = {}


def register_handler(event, widget, handler):
    print("REGISTER", event, widget.id, handler)
    _handlers[(event, widget.id)] = lambda: handler(widget)


def handle(event):
    print(f"Handle event {event.target.id}")
    try:
        handler = _handlers[('mouse_press', event.target.id.lstrip('toga_'))]
    except KeyError:
        print(f"No on_click handler {event.target.id}")
        return

    print(f"Invoking handler {handler}...")
    handler()
