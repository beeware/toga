import pytest

# import toga
from probe import get_probe
from tests.tests_backend.proxies.object_proxies import BoxProxy


@pytest.fixture
async def widget():
    raise NotImplementedError("test modules must define a `widget` fixture")


@pytest.fixture
async def probe(main_window, widget):
    old_content = main_window.content
    box = BoxProxy(children=[widget])
    main_window.content = box
    probe = get_probe(widget)
    yield probe
    main_window.content = old_content
