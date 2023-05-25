from unittest.mock import Mock

import pytest

import toga
from toga.style import Pack

from .properties import (  # noqa: F401
    test_flex_widget_size,
    test_focus,
)


@pytest.fixture
async def widget():
    return toga.WebView(style=Pack(flex=1))


async def test_load_url(widget, probe):
    on_webview_load_handler = Mock()
    widget.on_webview_load = on_webview_load_handler

    # Initial URL is empty
    assert widget.url is None
    await widget.load_url("https://github.com/beeware")

    # A short delay is required because HTML DOM evaluation lags.
    await probe.redraw("Page has loaded", delay=0.1)
    assert widget.url == "https://github.com/beeware"

    # The load hander was invoked.
    on_webview_load_handler.assert_called_once_with(widget)


async def test_static_content(widget, probe):
    "Static content can be loaded into the page"

    widget.set_content("https://example.com/", "<h1>Nice page</h1>")

    # A short delay is required because HTML DOM evaluation lags.
    await probe.redraw("Webview has static content", delay=0.1)

    assert widget.url == "https://example.com/"
    content = await probe.get_page_content()
    assert content == "<h1>Nice page</h1>"


async def test_user_agent(widget, probe):
    "The user agent can be customized"

    # Default user agents are a mess, but they all start with "Mozilla/5.0"
    assert widget.user_agent.startswith("Mozilla/5.0 (")

    # Set a custom user agent
    widget.user_agent = "NCSA_Mosaic/1.0"
    await probe.redraw("User agent has been customized")
    assert widget.user_agent == "NCSA_Mosaic/1.0"


async def test_evaluate_javascript(widget, probe):
    "JavaScript can be evaluated"
    on_result_handler = Mock()

    result = await widget.evaluate_javascript("37 + 42", on_result=on_result_handler)

    # The resulting value has been converted into Python
    assert result == 79
    # The same value was passed to the on-result handler
    on_result_handler.assert_called_once_with(79)


async def test_evaluate_javascript_no_handler(widget, probe):
    "A handler isn't needed to evaluate JavaScript"
    result = await widget.evaluate_javascript("37 + 42")

    # The resulting value has been converted into Python
    assert result == 79


async def test_evaluate_javascript_error(widget, probe):
    "If JavaScript content raises an error, the error is propegated"
    on_result_handler = Mock()

    with pytest.raises(RuntimeError):
        await widget.evaluate_javascript("not valid js", on_result=on_result_handler)

    # The same value was passed to the on-result handler
    on_result_handler.assert_called_once()
    assert on_result_handler.call_args.args[0] is None
    assert isinstance(on_result_handler.call_args.kwargs["exception"], RuntimeError)


async def test_evaluate_javascript_error_without_handler(widget, probe):
    "A handler isn't needed to propegate a JavaScript error"
    with pytest.raises(RuntimeError):
        await widget.evaluate_javascript("not valid js")
