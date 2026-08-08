import pytest

import toga


@pytest.fixture
def window(app):
    return toga.Window()
