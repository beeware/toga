from unittest.mock import Mock

import pytest
from probe import get_probe

import toga


@pytest.fixture
async def widget():
    raise NotImplementedError("test modules must define a `widget` fixture")


@pytest.fixture
async def probe(main_window, widget):
    old_content = main_window.content
    box = toga.Box(children=[widget])
    main_window.content = box
    probe = get_probe(widget)
    yield probe
    main_window.content = old_content


@pytest.fixture
async def other(widget):
    """A separate widget that can take focus"""
    other = toga.TextInput()
    widget.parent.add(other)
    return other


@pytest.fixture(params=[True, False])
async def focused(request, widget, other):
    if request.param:
        widget.focus()
    else:
        other.focus()
    return request.param


@pytest.fixture
async def on_change(widget):
    handler = Mock()
    widget.on_change = handler
    handler.assert_not_called()
    return handler
