# from pytest import fixture, register_assert_rewrite, skip
import pytest

import toga

pytest_plugins = ["tests.tests_backend.web_test_patch"]


@pytest.fixture(scope="session")
def app():
    return toga.App.app()


@pytest.fixture(scope="session")
def main_window(app):
    return app.main_window
