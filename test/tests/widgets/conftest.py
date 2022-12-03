from pytest import fixture

import toga

from .probe import get_probe


@fixture
async def widget():
    raise NotImplementedError("test modules must define a `widget` fixture")


@fixture
async def probe(main_window, widget):
    box = toga.Box(children=[widget])
    main_window.content = box
    yield get_probe(widget, box)
    # TODO: Window.content doesn't currently accept None.
    main_window.content = toga.Box()
