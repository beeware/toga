import asyncio
from asyncio import wait_for
from contextlib import nullcontext
from http.cookiejar import CookieJar
from time import time
from unittest.mock import ANY, Mock

import pytest

import toga
from toga.style import Pack

from .conftest import build_cleanup_test, safe_create
from .properties import (  # noqa: F401
    test_flex_widget_size,
    test_focus,
)

# These timeouts are loose because CI can be very slow, especially on mobile.
LOAD_TIMEOUT = 30
JS_TIMEOUT = 5
WINDOWS_INIT_TIMEOUT = 60


async def get_content(widget):
    # On Apple platforms while a page is still loading, document.body might return
    # null and cause the call to fail and error.  Handle that by returning None
    # otherwise.
    # On Android, if the same error happens, the callback will not be called and
    # cause an asyncio timeout error. This also avoids the error on Android by
    # returning null if there's no document.body.
    return await wait_for(
        widget.evaluate_javascript("document.body ? document.body.innerHTML : null"),
        JS_TIMEOUT,
    )


async def assert_content_change(widget, probe, message, url, content, on_load):
    # Web views aren't instantaneous. Even for simple static changes of page
    # content, the DOM won't be immediately rendered. As a result, even though a
    # page loaded signal has been received, it doesn't mean the accessors for
    # the page URL or DOM content has been updated in the widget. This is a
    # problem for tests, as we need to "make change, test change occurred" with
    # as little delay as possible. So - wait for up to 2 seconds for the URL
    # *and* content to change in any way before asserting the new values.

    changed = False
    timer = LOAD_TIMEOUT

    await probe.redraw(message)

    # Loop until a change occurs
    while timer > 0 and not changed:
        new_url = widget.url
        new_content = await get_content(widget)

        changed = new_url == url and new_content == content
        if not changed:
            timer -= 0.05
            await asyncio.sleep(0.05)

    if not changed:
        pytest.fail(f"{new_url=!r}, {url=!r}, {new_content[:50]=!r}, {content=!r}")

    if not probe.supports_on_load:
        on_load.assert_not_called()
    else:
        # Loop until an event occurs
        while timer > 0 and not on_load.mock_calls:
            timer -= 0.05
            await asyncio.sleep(0.05)
        on_load.assert_called_with(widget)


@pytest.fixture
async def on_load():
    on_load = Mock()
    return on_load


@pytest.fixture
async def widget(on_load):
    with safe_create():
        widget = toga.WebView(style=Pack(flex=1), on_webview_load=on_load)

    # We shouldn't be able to get a callback until at least one tick of the event loop
    # has completed.
    on_load.assert_not_called()

    # On Windows, the WebView has an asynchronous initialization process. Before we
    # start the test, make sure initialization is complete by checking the user agent.
    deadline = time() + WINDOWS_INIT_TIMEOUT
    while True:
        try:
            # Default user agents are a mess, but they all start with "Mozilla/5.0"
            ua = widget.user_agent
            assert ua.startswith("Mozilla/5.0 (")
            break
        except AssertionError:
            # On Windows, user_agent will return an empty string during initialization.
            if (
                toga.platform.current_platform == "windows"
                and ua == ""
                and time() < deadline
            ):
                await asyncio.sleep(0.05)
            else:
                raise

    yield widget

    if toga.backend == "toga_gtk":
        # On Gtk, ensure that the MapView evades garbage collection by keeping a
        # reference to it in the app. The WebKit2 WebView will raise a SIGABRT if the
        # thread disposing of it is not the same thread running the event loop. Since
        # garbage collection for the WebView can run in either thread, just defer GC
        # for it until after the testing thread has joined.
        toga.App.app._gc_protector.append(widget)


test_cleanup = build_cleanup_test(toga.WebView, xfail_backends=("toga_gtk",))


@pytest.mark.flaky(retries=5, delay=1)
async def test_set_url(widget, probe, on_load):
    """The URL can be set."""
    widget.url = "https://github.com/beeware"

    # Wait for the content to be loaded
    await assert_content_change(
        widget,
        probe,
        message="Page has been loaded",
        url="https://github.com/beeware",
        content=ANY,
        on_load=on_load,
    )


@pytest.mark.flaky(retries=5, delay=1)
async def test_clear_url(widget, probe, on_load):
    """The URL can be cleared."""
    widget.url = None

    # Wait for the content to be cleared
    await assert_content_change(
        widget,
        probe,
        message="Page has been cleared",
        url=None,
        content="",
        on_load=on_load,
    )


async def test_load_empty_url(widget, probe, on_load):
    """An empty URL can be loaded asynchronously into the view."""
    await wait_for(
        widget.load_url(None),
        LOAD_TIMEOUT,
    )

    # DOM loads aren't instantaneous; wait for the URL to appear
    await assert_content_change(
        widget,
        probe,
        message="Page has been cleared",
        url=None,
        content="",
        on_load=on_load,
    )


@pytest.mark.flaky(retries=5, delay=1)
async def test_load_url(widget, probe, on_load):
    """A URL can be loaded into the view."""
    await wait_for(
        widget.load_url("https://github.com/beeware"),
        LOAD_TIMEOUT,
    )

    # DOM loads aren't instantaneous; wait for the URL to appear
    await assert_content_change(
        widget,
        probe,
        message="Page has been loaded",
        url="https://github.com/beeware",
        content=ANY,
        on_load=on_load,
    )


async def test_static_content(widget, probe, on_load):
    """Static content can be loaded into the page."""
    widget.set_content("https://example.com/", "<h1>Nice page</h1>")

    # DOM loads aren't instantaneous; wait for the URL to appear
    await assert_content_change(
        widget,
        probe,
        message="Webview has static content",
        url="https://example.com/" if probe.content_supports_url else None,
        content="<h1>Nice page</h1>",
        on_load=on_load,
    )


async def test_static_large_content(widget, probe, on_load):
    """Static large content can be loaded into the page"""
    large_content = f"<p>{'lorem ipsum ' * 200000}</p>"
    url = "https://example.com/"
    widget.set_content(url, large_content)
    # some platforms handle large content by loading a file from the cache folder
    if hasattr(probe, "get_large_content_url"):  # pragma: no branch
        url = probe.get_large_content_url(widget)

    # DOM loads aren't instantaneous; wait for the URL to appear
    await assert_content_change(
        widget,
        probe,
        message="Webview has static large content",
        url=url,
        content=large_content,
        on_load=on_load,
    )


async def test_user_agent(widget, probe):
    "The user agent can be customized"

    # The default user agent is tested by the `widget` fixture.
    widget.user_agent = "NCSA_Mosaic/1.0"
    await probe.redraw("User agent has been customized")
    assert widget.user_agent == "NCSA_Mosaic/1.0"


@pytest.mark.flaky(retries=5, delay=1)
async def test_evaluate_javascript(widget, probe):
    """JavaScript can be evaluated."""
    on_result_handler = Mock()

    for expression, expected in [
        ("37 + 42", 79),
        ("'awesome'.includes('we')", True),
        ("'hello js'", "hello js"),
    ]:
        # reset the mock for each pass
        on_result_handler.reset_mock()

        with pytest.warns(
            DeprecationWarning,
            match=r"Synchronous `on_result` handlers have been deprecated;",
        ):
            result = await wait_for(
                widget.evaluate_javascript(expression, on_result=on_result_handler),
                JS_TIMEOUT,
            )

        # The resulting value has been converted into Python
        assert result == expected
        # The same value was passed to the on-result handler
        on_result_handler.assert_called_once_with(expected)


@pytest.mark.flaky(retries=5, delay=1)
async def test_evaluate_javascript_no_handler(widget, probe):
    """A handler isn't needed to evaluate JavaScript."""
    result = await wait_for(
        widget.evaluate_javascript("37 + 42"),
        JS_TIMEOUT,
    )

    # The resulting value has been converted into Python
    assert result == 79


def javascript_error_context(probe):
    if probe.javascript_supports_exception:
        return pytest.raises(RuntimeError)
    else:
        return nullcontext()


@pytest.mark.flaky(retries=5, delay=1)
async def test_evaluate_javascript_error(widget, probe):
    """If JavaScript content raises an error, the error is propagated."""
    on_result_handler = Mock()

    with javascript_error_context(probe):
        with pytest.warns(
            DeprecationWarning,
            match=r"Synchronous `on_result` handlers have been deprecated;",
        ):
            result = await wait_for(
                widget.evaluate_javascript("not valid js", on_result=on_result_handler),
                JS_TIMEOUT,
            )
        # If the backend supports exceptions, the previous line should have raised one.
        assert not probe.javascript_supports_exception
        assert result is None

    # The same value was passed to the on-result handler
    on_result_handler.assert_called_once()
    assert on_result_handler.call_args.args == (None,)
    kwargs = on_result_handler.call_args.kwargs
    if probe.javascript_supports_exception:
        assert sorted(kwargs) == ["exception"]
        assert isinstance(kwargs["exception"], RuntimeError)
    else:
        assert kwargs == {}


@pytest.mark.flaky(retries=5, delay=1)
async def test_evaluate_javascript_error_without_handler(widget, probe):
    """A handler isn't needed to propagate a JavaScript error."""
    with javascript_error_context(probe):
        result = await wait_for(
            widget.evaluate_javascript("not valid js"),
            JS_TIMEOUT,
        )
        # If the backend supports exceptions, the previous line should have raised one.
        assert not probe.javascript_supports_exception
        assert result is None


@pytest.mark.flaky(retries=5, delay=1)
async def test_dom_storage_enabled(widget, probe, on_load):
    """Ensure DOM storage is enabled."""
    # a page must be loaded to access local storage
    await wait_for(
        widget.load_url("https://github.com/"),
        LOAD_TIMEOUT,
    )

    for _ in range(10):
        expected_value = "Hello World"
        expression = f"""\
    (function isLocalStorageAvailable(){{
        var test = 'testkey';
        try {{
            localStorage.setItem(test, "{expected_value}");
            item = localStorage.getItem(test);
            localStorage.removeItem(test);
            return item;
        }} catch(e) {{
            return String(e);
        }}
    }})()"""
        result = await wait_for(widget.evaluate_javascript(expression), JS_TIMEOUT)
        if result == expected_value:
            # Success!
            return

        await probe.redraw("Wait for DOM to be ready", delay=0.2)

    pytest.fail(
        f"Didn't receive expected result ({expected_value!r}) after multiple tries; "
        f"last attempt returned {result!r}"
    )


@pytest.mark.flaky(retries=5, delay=1)
async def test_retrieve_cookies(widget, probe, on_load):
    """Cookies can be retrieved."""
    # A page must be loaded to set cookies
    await wait_for(
        widget.load_url("https://github.com/beeware"),
        LOAD_TIMEOUT,
    )
    # DOM loads aren't instantaneous; wait for the URL to appear
    await assert_content_change(
        widget,
        probe,
        message="Page has been loaded",
        url="https://github.com/beeware",
        content=ANY,
        on_load=on_load,
    )

    # On iOS and macOS, setting a cookie can fail if it's done too soon after page load.
    # Try a couple of times to make sure the cookie is actually set.
    for _ in range(5):
        # JavaScript expression to set a cookie and return the current cookies
        expression = """
        (function setCookie() {
            document.cookie = "test=test_value; path=/; Secure; SameSite=None";
            return document.cookie;
        })()"""

        await wait_for(widget.evaluate_javascript(expression), JS_TIMEOUT)

        # Retrieve cookies.
        cookie_jar = await widget.cookies

        assert isinstance(cookie_jar, CookieJar)

        # Cookie retrieval isn't implemented on every backend (yet), so we implement the
        # retrieval in the probe to provide an opportunity to skip the test.
        cookie = probe.extract_cookie(cookie_jar, "test")

        if cookie is None:
            # Cookie wasn't set; wait a little bit before trying again.
            await probe.redraw("Cookie wasn't set; wait and try again", delay=0.2)

    assert cookie is not None, "Test cookie not found in CookieJar"

    # Validate the test cookie
    assert cookie.name == "test"
    assert cookie.value == "test_value"
    assert cookie.domain == "github.com"
    assert cookie.path == "/"
    assert cookie.secure is True
    assert cookie.expires is None


@pytest.mark.flaky(retries=5, delay=1)
async def test_on_navigation_starting_sync_no_handler(widget, probe, on_load):
    # This test is required for full coverage because on android, setting
    # the URL does not trigger shouldOverrideUrlLoading()
    await widget.evaluate_javascript('window.location.assign("https://beeware.org/")')
    await asyncio.sleep(5)
    await widget.evaluate_javascript(
        'window.location.assign("https://beeware.org/docs/")'
    )
    await asyncio.sleep(5)
    assert widget.url == "https://beeware.org/docs/"


@pytest.mark.flaky(retries=5, delay=1)
async def test_on_navigation_starting_sync(widget, probe, on_load):
    if not getattr(widget._impl, "SUPPORTS_ON_NAVIGATION_STARTING", True):
        pytest.skip("Platform doesn't support on_navigation_starting")

    # Allow navigation to any beeware.org URL.
    def handler(widget, url, **kwargs):
        return url.startswith("https://beeware.org/")

    widget.on_navigation_starting = handler

    # test static content can be set
    widget.set_content("https://example.com/", "<h1>Nice page</h1>")
    # DOM loads aren't instantaneous; wait for the URL to appear
    await assert_content_change(
        widget,
        probe,
        message="Webview has static content",
        url="https://example.com/" if probe.content_supports_url else None,
        content="<h1>Nice page</h1>",
        on_load=on_load,
    )

    # test static content can be set with no URL
    widget.set_content(None, "<h1>Other page</h1>")
    # DOM loads aren't instantaneous; wait for the URL to appear
    await assert_content_change(
        widget,
        probe,
        message="Webview has static content with no URL",
        url=None,
        content="<h1>Other page</h1>",
        on_load=on_load,
    )

    # test url allowed by code
    await wait_for(
        widget.load_url("https://github.com/beeware/"),
        LOAD_TIMEOUT,
    )
    # DOM loads aren't instantaneous; wait for the URL to appear
    await assert_content_change(
        widget,
        probe,
        message="Page has been loaded",
        url="https://github.com/beeware/",
        content=ANY,
        on_load=on_load,
    )

    assert widget.url == "https://github.com/beeware/"
    # simulate browser navigation to denied url
    await widget.evaluate_javascript(
        'window.location.assign("https://github.com/beeware/toga/")'
    )
    await probe.redraw("Attempt to navigate to forbidden URL", delay=5)

    assert widget.url == "https://github.com/beeware/"
    # simulate browser navigation to allowed url
    await widget.evaluate_javascript(
        'window.location.assign("https://beeware.org/docs/")'
    )
    await probe.redraw("Attempt to navigate to allowed URL", delay=5)
    assert widget.url == "https://beeware.org/docs/"

    # The webview can always be cleared to no URL
    widget.url = None
    # Wait for the content to be cleared
    await assert_content_change(
        widget,
        probe,
        message="Page has been cleared",
        url=None,
        content="",
        on_load=on_load,
    )


@pytest.mark.flaky(retries=5, delay=1)
async def test_on_navigation_starting_async(widget, probe, on_load):
    if not getattr(widget._impl, "SUPPORTS_ON_NAVIGATION_STARTING", True):
        pytest.skip("Platform doesn't support on_navigation_starting")

    async def handler(widget, url, **kwargs):
        return url.startswith("https://beeware.org/")

    widget.on_navigation_starting = handler
    # test static content can be set
    widget.set_content("https://example.com/", "<h1>Nice page</h1>")
    # DOM loads aren't instantaneous; wait for the URL to appear
    await assert_content_change(
        widget,
        probe,
        message="Webview has static content",
        url="https://example.com/" if probe.content_supports_url else None,
        content="<h1>Nice page</h1>",
        on_load=on_load,
    )
    # test url allowed by code
    await wait_for(
        widget.load_url("https://github.com/beeware/"),
        LOAD_TIMEOUT,
    )
    # DOM loads aren't instantaneous; wait for the URL to appear
    await assert_content_change(
        widget,
        probe,
        message="Page has been loaded",
        url="https://github.com/beeware/",
        content=ANY,
        on_load=on_load,
    )

    assert widget.url == "https://github.com/beeware/"

    # simulate browser navigation to denied url
    await widget.evaluate_javascript(
        'window.location.assign("https://github.com/beeware/toga/")'
    )
    await probe.redraw("Attempt to navigate to denied URL", delay=5)
    assert widget.url == "https://github.com/beeware/"

    # simulate browser navigation to allowed url
    await widget.evaluate_javascript(
        'window.location.assign("https://beeware.org/docs/")'
    )
    await probe.redraw("Attempt to navigate to allowed URL", delay=5)
    assert widget.url == "https://beeware.org/docs/"
