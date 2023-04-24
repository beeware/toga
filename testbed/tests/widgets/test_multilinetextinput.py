import pytest

import toga

from ..conftest import skip_on_platforms


@pytest.fixture
async def widget():
    skip_on_platforms("android", "windows", "linux")
    return toga.MultilineTextInput(value="Hello")


async def test_readonly(widget, probe):
    "A widget can be made readonly"
    # Initial value is enabled
    assert not widget.readonly
    assert not probe.readonly

    # Change to readonly
    widget.readonly = True
    await probe.redraw(message="Multiline Text Input should be read only")

    assert widget.readonly
    assert probe.readonly

    # Change back to writable
    widget.readonly = False
    await probe.redraw(message="Multiline Text Input should be writable")

    assert not widget.readonly
    assert not probe.readonly
