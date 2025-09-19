# from pytest import fixture, register_assert_rewrite, skip
# import toga

import pytest

from .tests_backend.playwright_page import BackgroundPage
from .tests_backend.proxies.app_proxy import AppProxy

# In future, would only need to be BaseProxy and SimpleProbe/BaseProbe.
from .tests_backend.proxies.base_proxy import BaseProxy
from .tests_backend.widgets.button import ButtonProbe


@pytest.fixture(scope="session")
def page():
    p = BackgroundPage()
    return p


# In future, will only be BaseProxy and BaseProbe/SimpleProbe
@pytest.fixture(scope="session", autouse=True)
def _wire_page(page):
    BaseProxy.page_provider = staticmethod(lambda: page)
    ButtonProbe.page_provider = staticmethod(lambda: page)


@pytest.fixture(scope="session")
def app():
    # just return AppProxy
    return AppProxy()


@pytest.fixture(scope="session")
def main_window(app):
    # return main window created by app proxy
    return app.main_window
