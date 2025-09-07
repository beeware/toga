# from pytest import fixture, register_assert_rewrite, skip
# import toga

import pytest

from .tests_backend.page_singleton import BackgroundPage

# In future, would only need to be AppProxy, MainWindowProxy, ProxyBase and
# a SimpleProbe/BaseProbe.
# Possibly only ProxyBase and SimpleProbe/BaseProbe.
from .tests_backend.proxies.app_proxy import AppProxy
from .tests_backend.proxies.base_proxy import BaseProxy
from .tests_backend.proxies.box_proxy import BoxProxy
from .tests_backend.proxies.main_window_proxy import MainWindowProxy
from .tests_backend.widgets.button import ButtonProbe


# With this page injection method, we could possibly extend so that
# multiple pages can be created and be running at once (if it is ever
# needed in the future). Would need to add a method/fixture to store
# and switch between them.
@pytest.fixture(scope="session")
def page():
    p = BackgroundPage()
    yield p


@pytest.fixture(scope="session", autouse=True)
def _wire_page(page):
    BaseProxy.page_provider = staticmethod(lambda: page)
    BoxProxy.page_provider = staticmethod(lambda: page)
    MainWindowProxy.page_provider = staticmethod(lambda: page)
    ButtonProbe.page_provider = staticmethod(lambda: page)


@pytest.fixture(scope="session")
def app():
    # just return AppProxy
    return AppProxy()


@pytest.fixture(scope="session")
def main_window(app):
    # return main window created by app proxy
    return app.main_window
