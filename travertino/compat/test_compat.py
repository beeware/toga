####################################################################################
# The following tests check that the current version of Travertino being tested works
# correctly with Toga 0.4.8
####################################################################################
from unittest.mock import Mock, call

import pytest
import toga
from toga.style.pack import Pack
from toga_demo import app


def test_reapply():
    """Calling reapply() is rerouted to the old apply(name, value) signature."""
    box = toga.Box()
    mock = Mock(wraps=box.style.apply)
    box.style.apply = mock
    with pytest.warns(DeprecationWarning):
        box.style.reapply()

    assert sorted(mock.mock_calls) == [
        call("alignment", None),
        call("background_color", None),
        call("color", None),
        call("direction", "row"),
        call("display", "pack"),
        call("flex", 0.0),
        call("font_family", "system"),
        call("font_size", -1),
        call("font_style", "normal"),
        call("font_variant", "normal"),
        call("font_weight", "normal"),
        call("height", "none"),
        call("padding_bottom", 0),
        call("padding_left", 0),
        call("padding_right", 0),
        call("padding_top", 0),
        call("text_align", None),
        call("text_direction", "ltr"),
        call("visibility", "visible"),
        call("width", "none"),
    ]


def test_validated_set_delete():
    """Setting or deleting a property results in the proper method calls.

    Each will first call the newer apply(name) signature, which is then rerouted to
    apply(name, value).
    """
    style = Pack()
    mock = Mock(wraps=style.apply)
    style.apply = mock
    style.font_size = 10
    assert style.apply.mock_calls == [call("font_size"), call("font_size", 10)]
    mock.reset_mock()
    del style.font_size
    assert style.apply.mock_calls == [call("font_size"), call("font_size", -1)]


def test_invalid_property_in_init():
    """An invalid keyword raises a TypeError, like it would in the dataclass."""
    with pytest.raises(
        TypeError,
        match=r"Pack.__init__\(\) got an unexpected keyword argument 'fake_name'",
    ):
        _ = Pack(fake_name=False)


def test_demo():
    """The demo app can start up (with the demo backend).

    This doesn't actually generate any deprecation warnings, because they've already
    been emitted when importing Toga. But this confirms that, at the very least, the
    demo app can run through its startup method without generating any uncaught
    exceptions.

    The dummy backend is set via environment variable (and the actual backend shouldn't
    even be installed), so this is nonblocking; it simply runs through the startup
    process, goes through the motions of calculating layout and such, then exits.
    """
    app.main().main_loop()
