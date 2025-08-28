#from pytest import fixture, register_assert_rewrite, skip
#import toga

import pytest
from .tests_backend.proxies.app_proxy import AppProxy

@pytest.fixture(scope="session")
def app():
    # just return AppProxy
    return AppProxy()

@pytest.fixture(scope="session")
def main_window(app):
    # return main window created by app proxy
    return app.main_window