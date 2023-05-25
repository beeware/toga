import asyncio
from unittest.mock import Mock

import pytest

import toga
from toga.widgets.webview import JavaScriptResult
from toga_dummy.utils import (
    assert_action_performed,
    assert_action_performed_with,
    attribute_value,
)


@pytest.fixture
def widget():
    return toga.WebView()


def test_widget_created():
    "A WebView can be created with minimal arguments"
    widget = toga.WebView()

    assert widget._impl.interface == widget
    assert_action_performed(widget, "create WebView")

    assert widget.url is None
    assert widget.user_agent == "Toga dummy backend"
    assert widget._on_webview_load._raw is None


def test_create_with_values():
    "A WebView can be created with initial values"
    on_webview_load = Mock()

    widget = toga.WebView(
        url="https://beeware.org",
        user_agent="Custom agent",
        on_webview_load=on_webview_load,
    )
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create WebView")

    assert widget.url == "https://beeware.org"
    assert widget.user_agent == "Custom agent"
    assert widget.on_webview_load._raw == on_webview_load


# class WebViewTests(TestCase):
#     def setUp(self):
#         super().setUp()

#         self.url = "https://beeware.org/"

#         def callback(widget):
#             pass

#         self.on_key_press = callback
#         self.web_view = toga.WebView(
#             url=self.url, on_key_press=self.on_key_press, user_agent="DUMMY AGENT"
#         )

#     def test_widget_created(self):
#         self.assertEqual(self.web_view._impl.interface, self.web_view)
#         self.assertActionPerformed(self.web_view, "create WebView")

#     def test_setting_url_invokes_impl_method(self):
#         new_url = "https://github.com/"
#         self.web_view.url = new_url
#         self.assertEqual(self.web_view.url, new_url)
#         self.assertValueSet(self.web_view, "url", new_url)

#     def test_set_content_invokes_impl_method(self):
#         root_url = "https://github.com/"
#         new_content = """<!DOCTYPE html>
#             <html>
#               <body>
#                 <h1>My First Heading</h1>
#                 <p>My first paragraph.</p>
#               </body>
#             </html>
#         """

#         self.web_view.set_content(root_url, new_content)
#         self.assertActionPerformedWith(
#             self.web_view, "set content", root_url=root_url, content=new_content
#         )

#     def test_get_dom(self):
#         dom = self.web_view.dom
#         self.assertEqual(dom, "DUMMY DOM")
#         self.assertActionPerformed(self.web_view, "get DOM")


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com",
        "https://example.com",
        None,
    ],
)
def test_url(widget, url):
    "The URL of a webview can be set"
    # Set up a load handler
    on_webview_load_handler = Mock()
    widget.on_webview_load = on_webview_load_handler

    widget.url = url
    assert widget.url == url

    # There's no future created for the load.
    assert attribute_value(widget, "loaded_future") is None

    # The load handler hasn't been called yet
    on_webview_load_handler.assert_not_called()

    # Simulate a page load
    widget._impl.simulate_page_loaded()

    # handler has been invoked
    on_webview_load_handler.assert_called_once_with(widget)


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com",
        "https://example.com",
        None,
    ],
)
async def test_load_url(widget, url):
    "The URL of a webview can be loaded asynchronously"
    # Set up a load handler
    on_webview_load_handler = Mock()
    widget.on_webview_load = on_webview_load_handler

    # An async task that simulates a page load after a delay
    async def delayed_page_load():
        await asyncio.sleep(0.1)

        # There should be a pending future
        loaded_future = attribute_value(widget, "loaded_future")
        assert asyncio.isfuture(loaded_future)

        # Complete the page load
        widget._impl.simulate_page_loaded()

        # The loading result is None
        assert loaded_future.result() is None

    asyncio.create_task(delayed_page_load())

    # wait for a URL to load
    await widget.load_url(url)

    # The URL has been set
    assert widget.url == url

    # The handler has been invoked
    on_webview_load_handler.assert_called_once_with(widget)

    # The future has been cleared
    assert attribute_value(widget, "loaded_future") is None


@pytest.mark.parametrize(
    "url",
    [
        "file:///Path/to/file",
        "gopher://example.com",
    ],
)
async def test_invalid_url(widget, url):
    "URLs must start with https:// or http://"
    with pytest.raises(
        ValueError,
        match=r"WebView can only display http:// and https:// URLs",
    ):
        widget.url = url

    with pytest.raises(
        ValueError,
        match=r"WebView can only display http:// and https:// URLs",
    ):
        await widget.load_url(url)


def test_set_content(widget):
    "Static HTML content can be loaded into the page"
    widget.set_content("https://example.com", "<h1>Fancy page</h1>")
    assert_action_performed_with(
        widget, "set_content", "https://example.com", "<h1>Fancy page</h1>"
    )


def test_user_agent(widget):
    "The user agent can be customized"
    widget.user_agent = "New user agent"
    assert widget.user_agent == "New user agent"


def test_evaluate_javascript(widget):
    "Javascript can be evaluated"
    result = widget.evaluate_javascript("test(1);")
    assert_action_performed(widget, "evaluate_javascript")

    assert isinstance(result, JavaScriptResult)

    # Attempting to use or compare the result raises an error
    with pytest.raises(
        RuntimeError,
        match=r"Can't check JavaScript result directly; use await or an on_result handler",
    ):
        result == 42


async def test_evaluate_javascript_async(widget):
    "Javascript can be evaluated asyncronously, and an asynchronous result returned"

    # An async task that simulates evaluation of javasript after a delay
    async def delayed_page_load():
        await asyncio.sleep(0.1)

        # Complete the Javascript
        widget._impl.simulate_javascript_result(42)

    asyncio.create_task(delayed_page_load())

    result = await widget.evaluate_javascript("test(1);")
    assert_action_performed(widget, "evaluate_javascript")

    assert result == 42
