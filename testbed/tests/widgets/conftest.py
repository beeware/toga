import gc
import os
import weakref
from contextlib import contextmanager
from unittest.mock import Mock

import pytest

import toga
from toga.style.pack import TOP

from ..conftest import (
    skip_on_backends,
    skip_on_platforms,
    xfail_on_backends,
    xfail_on_platforms,
)
from .probe import get_probe


@pytest.fixture
async def widget():
    raise NotImplementedError("test modules must define a `widget` fixture")


@pytest.fixture
async def probe(main_window, widget):
    old_content = main_window.content

    box = toga.Box(children=[widget])
    main_window.content = box
    probe = get_probe(widget)
    await probe.redraw(f"\nConstructing {widget.__class__.__name__} probe")
    probe.assert_container(box)
    yield probe

    main_window.content = old_content


@pytest.fixture
async def container_probe(widget):
    return get_probe(widget.parent)


@pytest.fixture
async def other(widget):
    """A separate widget that can take focus"""
    other = toga.TextInput()
    widget.parent.add(other)
    return other


@pytest.fixture
async def other_probe(other):
    return get_probe(other)


@pytest.fixture(params=[True, False])
async def focused(request, widget, other):
    if request.param:
        widget.focus()
    else:
        other.focus()
    return request.param


@pytest.fixture
async def on_change(widget):
    on_change = Mock()
    widget.on_change = on_change
    on_change.assert_not_called()
    return on_change


@pytest.fixture
def verify_font_sizes():
    """Whether the widget's width and height are affected by font size"""
    return True, True


@pytest.fixture
def verify_focus_handlers():
    """Whether the widget has on_gain_focus and on_lose_focus handlers"""
    return False


@pytest.fixture
def verify_vertical_text_align():
    """The widget's default vertical text alignment"""
    return TOP


@contextmanager
def safe_create():
    """A context manager to protect against widgets that can't be instantiated.

    Catches RuntimeErrors, and:
    * skips if the exception message contains the content "isn't supported on"
      (e.g., "WebView isn't supported on GTK4");
    * xfails if running outside a CI environment (this likely indicates a
      missing system requirement)
    * re-raises if in CI environment (since the CI environment *should* have
      all system requirements installed)
    """
    try:
        yield
    except RuntimeError as e:
        msg = str(e)
        if " isn't supported on " in msg:
            # If the widget fails because the platform doesn't support it, we
            # can skip the test.
            pytest.skip(msg)
        elif os.getenv("CI", None) is None:
            # If we're on the user's machine (i.e., *not* in a CI environment),
            # they might not have the required dependencies installed - in which
            # case that's an expected failure.
            pytest.xfail(msg)
        else:
            raise


def build_cleanup_test(
    widget_constructor,
    args=None,
    kwargs=None,
    skip_platforms=(),
    xfail_platforms=(),
    skip_backends=(),
    xfail_backends=(),
):
    async def test_cleanup():
        skip_on_platforms(*skip_platforms)
        xfail_on_platforms(*xfail_platforms, reason="Leaks memory")
        skip_on_backends(*skip_backends)
        xfail_on_backends(*xfail_backends, reason="Leaks memory")

        local_args = () if args is None else args
        local_kwargs = {} if kwargs is None else kwargs

        with safe_create():
            widget = widget_constructor(*local_args, **local_kwargs)
        ref = weakref.ref(widget)
        # Break potential reference cycles
        del widget, local_args, local_kwargs
        gc.collect()
        assert ref() is None

    return test_cleanup
