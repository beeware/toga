import pytest

import toga


@pytest.fixture
async def widget():
    return toga.PasswordInput(value="sekrit")


@pytest.fixture
def verify_font_sizes():
    # We can't verify font width inside the TextInput
    return False, True


async def test_value_hidden(widget, probe):
    "Value should always be hidden in a PasswordInput"
    assert probe.value_hidden

    widget.value = ""
    await probe.redraw("Value changed from non-empty to empty")
    assert probe.value_hidden

    widget.value = "something"
    await probe.redraw("Value changed from empty to non-empty")
    assert probe.value_hidden
