from unittest.mock import Mock

import pytest

import toga
from toga_dummy.utils import assert_action_not_performed, assert_action_performed


@pytest.fixture
def renderer():
    renderer = Mock()
    # renderer.on_init = Mock()
    # renderer.on_render = Mock()
    return renderer


@pytest.fixture
def widget(renderer):
    return toga.OpenGLView(renderer)


def test_widget_created(renderer):
    """An OpenGLView can be created."""
    widget = toga.OpenGLView(renderer)
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create OpenGLView")
    renderer.on_init.assert_called_once_with(widget)


def test_disable_no_op(widget):
    """OpenGLView doesn't have a disabled state."""
    # Enabled by default
    assert widget.enabled

    # Try to disable the widget
    widget.enabled = False

    # Still enabled.
    assert widget.enabled


def test_focus_noop(widget):
    """Focus is a no-op."""

    widget.focus()
    assert_action_not_performed(widget, "focus")


def test_redraw(widget, renderer):
    """The canvas can be redrawn."""
    widget.redraw()

    assert_action_performed(widget, "redraw")
    renderer.on_render.assert_called_once_with(widget, (37, 42))
