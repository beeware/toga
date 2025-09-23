# from pytest import fixture, register_assert_rewrite, skip
# import toga

import pytest

from .tests_backend.playwright_page import BackgroundPage
from .tests_backend.proxies.app_proxy import AppProxy
from .tests_backend.proxies.base_proxy import BaseProxy
from .tests_backend.widgets.base import SimpleProbe


@pytest.fixture(scope="session")
def page():
    p = BackgroundPage()
    return p


# Inject Playwright page object into
@pytest.fixture(scope="session", autouse=True)
def _wire_page(page):
    BaseProxy.page_provider = staticmethod(lambda: page)
    SimpleProbe.page_provider = staticmethod(lambda: page)


@pytest.fixture(scope="session")
def app():
    return AppProxy()


@pytest.fixture(scope="session")
def main_window(app):
    return app.main_window
