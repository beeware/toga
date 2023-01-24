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

    probe = get_probe(widget)
    await probe.redraw()
    probe.assert_container(box)

    yield probe

    main_window.content = toga.Box()
