import pytest
from pytest import fixture

import toga

if toga.platform.current_platform not in {"macOS", "iOS"}:
    pytest.skip("tests are not implemented for platform", allow_module_level=True)


@fixture
def readonly():
    """Provide default value for `readonly`"""
    return None


@fixture
async def widget(readonly):
    kwargs = {}
    if readonly is not None:
        kwargs["readonly"] = readonly
    return toga.MultilineTextInput(value="Hello", **kwargs)


@pytest.mark.parametrize("readonly", [True, False, None])
async def test_readonly_on_init(widget, probe, readonly):
    "`readonly` parameter enables or disables the widget"
    if readonly is None:
        readonly = False

    assert widget.readonly == readonly
    assert probe.enabled == (not readonly)
