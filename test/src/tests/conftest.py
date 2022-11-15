import toga_test.app
from pytest import fixture


@fixture
def app():
    return toga_test.app.app


@fixture
def main_window(app):
    return app.main_window


@fixture
def main_box(app):
    return app.main_box


@fixture
def native(widget):
    return widget._impl.native
