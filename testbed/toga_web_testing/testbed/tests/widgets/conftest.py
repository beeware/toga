import pytest
#import toga
from probe import get_probe
#from .probe import get_probe
from tests.tests_backend.proxies.box_proxy import BoxProxy
#from ..tests_backend.proxies.box_proxy import BoxProxy

""" TODO: Don't enable until below is implemented.
@pytest.fixture
async def widget():
    raise NotImplementedError("test modules must define a `widget` fixture")
"""

@pytest.fixture
async def probe(main_window, widget):
    old_content = main_window.content
    box = BoxProxy(children=[widget])
    main_window.content = box
    probe = get_probe(widget)
    yield probe
    main_window.content = old_content
    