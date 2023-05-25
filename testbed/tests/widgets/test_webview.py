import asyncio
from unittest.mock import ANY, Mock

import pytest

import toga
from toga.style import Pack

from .properties import (  # noqa: F401
    test_flex_widget_size,
    test_focus,
)


async def assert_content_change(widget, probe, message, url, content):
    # Web views aren't instantaneous. Even for simple static changes of page
    # content, the DOM won't be immediately rendered. As a result, even though a
    # page loaded signal has been received, it doesn't mean the accessors for
    # the page URL or DOM content has been updated in the widget. This is a
    # problem for tests, as we need to "make change, test change occurred" with
    # as little delay as possible. So - wait for up to 2 seconds for the URL
    # *and* content to change in any way before asserting the new values.

    changed = False
    timer = 2

    await probe.redraw(message)

    # Loop for up to a second for a change to occur
    while timer > 0 and not changed:
        new_url = widget.url
        new_content = await probe.get_page_content()

        changed = new_url == url and new_content == content
        if not changed:
            timer -= 0.05
            await asyncio.sleep(0.05)

    assert new_url == url
    assert new_content == content


@pytest.fixture
async def widget():
    widget = toga.WebView(style=Pack(flex=1))

    # Set some initial content that has a visible background
    widget.set_content(
        "https://example.com/",
        "<html style='background-color:rebeccapurple;'></html>",
    )
    return widget


async def test_clear_url(widget, probe):
    "The URL can be cleared"
    on_webview_load_handler = Mock()
    widget.on_webview_load = on_webview_load_handler

    widget.url = None

    # Wait for the content to be cleared
    await assert_content_change(
        widget,
        probe,
        message="Page has been cleared",
        url=None,
        content="",
    )

    # The load hander was invoked.
    on_webview_load_handler.assert_called_with(widget)


async def test_load_url(widget, probe):
    "A URL can be loaded into the view"
    on_webview_load_handler = Mock()
    widget.on_webview_load = on_webview_load_handler

    await widget.load_url("https://github.com/beeware")

    # DOM loads aren't instantaneous; wait for the URL to appear
    await assert_content_change(
        widget,
        probe,
        message="Page has been loaded",
        url="https://github.com/beeware",
        content=ANY,
    )

    # The load hander was invoked.
    on_webview_load_handler.assert_called_with(widget)


async def test_static_content(widget, probe):
    "Static content can be loaded into the page"
    on_webview_load_handler = Mock()
    widget.on_webview_load = on_webview_load_handler

    widget.set_content("https://example.com/", "<h1>Nice page</h1>")

    # DOM loads aren't instantaneous; wait for the URL to appear
    await assert_content_change(
        widget,
        probe,
        message="Webview has static content",
        url="https://example.com/",
        content="<h1>Nice page</h1>",
    )

    # The load hander was invoked.
    on_webview_load_handler.assert_called_with(widget)


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

    for expression, expected in [
        ("37 + 42", 79),
        ("'awesome'.includes('we')", True),
        ("'hello js'", "hello js"),
    ]:
        # reset the mock for each pass
        on_result_handler.reset_mock()

        result = await widget.evaluate_javascript(
            expression,
            on_result=on_result_handler,
        )

        # The resulting value has been converted into Python
        assert result == expected
        # The same value was passed to the on-result handler
        on_result_handler.assert_called_once_with(expected)


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
