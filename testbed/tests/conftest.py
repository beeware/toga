import asyncio
import gc
import inspect
from dataclasses import dataclass
from importlib import import_module

from pytest import fixture, register_assert_rewrite, skip

import toga
from toga.colors import GOLDENROD
from toga.constants import WindowState
from toga.style import Pack

# Ideally, we'd register rewrites for "tests" and get all the submodules
# recursively; however we've already imported "tests", so that raises a warning.
register_assert_rewrite("tests.assertions")
register_assert_rewrite("tests.widgets")
register_assert_rewrite("tests_backend")


# Use this for widgets or tests which are not supported on some platforms,
# but could be supported in the future.
def skip_on_platforms(*platforms, reason=None, allow_module_level=False):
    current_platform = toga.platform.current_platform
    if current_platform in platforms:
        skip(
            reason or f"not yet implemented on {current_platform}",
            allow_module_level=allow_module_level,
        )


# Use this for widgets or tests which are not supported on some backends,
# but could be supported in the future.
def skip_on_backends(*backends, reason=None, allow_module_level=False):
    current_backend = toga.backend
    if current_backend in backends:
        skip(
            reason or f"not yet implemented on {current_backend}",
            allow_module_level=allow_module_level,
        )


# Use this for widgets or tests which are not supported on some platforms,
# and will not be supported in the foreseeable future.
def xfail_on_platforms(*platforms, reason=None):
    current_platform = toga.platform.current_platform
    if current_platform in platforms:
        skip(reason or f"not applicable on {current_platform}")


# Use this for widgets or tests which are not supported on some backends,
# and will not be supported in the foreseeable future.
def xfail_on_backends(*backends, reason=None):
    current_backend = toga.platform.get_platform_factory().__package__
    if current_backend in backends:
        skip(reason or f"not applicable on {current_backend}")


# Use this for widgets or tests which trip up macOS privacy controls, and requires
# properties or entitlements defined in Info.plist
def skip_if_unbundled_app(reason=None, allow_module_level=False):
    if not toga.App.app.is_bundled:
        skip(
            reason
            or (
                "test requires a full application, "
                "use 'briefcase run' instead of 'briefcase dev'"
            ),
            allow_module_level=allow_module_level,
        )


@fixture(autouse=True)
def no_dangling_tasks():
    """Ensure any tasks for the test were removed when the test finished."""
    yield
    if toga.App.app:
        tasks = toga.App.app._running_tasks
        assert not tasks, f"the app has dangling tasks: {tasks}"


@fixture(scope="session")
def app():
    return toga.App.app


@fixture
async def app_probe(app):
    module = import_module("tests_backend.app")
    probe = module.AppProbe(app)

    if app.run_slow:
        print("\nConstructing app probe")
    yield probe

    # Force a GC pass on the main thread. This isn't perfect, but it helps
    # minimize garbage collection on the test thread.
    gc.collect()

    # Reset the command action mock
    app.cmd_action.reset_mock()


@fixture(scope="session")
def main_window(app):
    return app.main_window


@fixture(autouse=True)
async def window_cleanup(app, app_probe, main_window, main_window_probe):
    original_size = main_window.size

    # Ensure that at the beginning of every test, all windows that aren't
    # the main window have been closed and deleted. This needs to be done in
    # 2 passes because we can't modify the list while iterating over it.
    kill_list = []
    for window in app.windows:
        if window != main_window:
            kill_list.append(window)

    # Then purge everything on the kill list.
    while kill_list:
        window = kill_list.pop()
        probe = import_module("tests_backend.window").WindowProbe(app, window)
        await probe.cleanup()
        del window

    # Force a GC pass on the main thread. This isn't perfect, but it helps
    # minimize garbage collection on the test thread.
    gc.collect()

    main_window.state = WindowState.NORMAL
    app.current_window = main_window
    await main_window_probe.wait_for_window(
        "Resetting main_window", state=WindowState.NORMAL
    )

    yield

    # Reset the window state and size.
    main_window.state = WindowState.NORMAL
    main_window.size = original_size


@fixture(scope="session")
async def main_window_probe(app, main_window):
    old_content = main_window.content

    # Put something in the content window so that we know it's an app test
    main_window.content = toga.Box(style=Pack(background_color=GOLDENROD))

    module = import_module("tests_backend.window")
    if app.run_slow:
        print("\nConstructing Window probe")
    yield module.WindowProbe(app, main_window)

    main_window.content = old_content


# Controls the event loop used by pytest-asyncio.
@fixture(scope="session")
def event_loop_policy(app):
    yield ProxyEventLoopPolicy(ProxyEventLoop(app._impl.loop))


# Loop policy that ensures proxy loop is always used.
class ProxyEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    def __init__(self, proxy_loop: "ProxyEventLoop"):
        super().__init__()
        self._proxy_loop = proxy_loop

    def new_event_loop(self):
        return self._proxy_loop


# Proxy which forwards all tasks to another event loop in a thread-safe manner.
# It implements only the methods used by pytest-asyncio.
@dataclass
class ProxyEventLoop(asyncio.AbstractEventLoop):
    loop: object
    closed: bool = False

    # Used by ensure_future.
    def create_task(self, coro, **kwargs):
        return ProxyTask(coro, kwargs)

    def run_until_complete(self, future):
        if inspect.iscoroutine(future):
            coro = future
        elif isinstance(future, ProxyTask):
            coro = future.coro
        else:
            raise TypeError(f"Future type {type(future)} is not currently supported")
        return asyncio.run_coroutine_threadsafe(coro, self.loop).result()

    async def shutdown_asyncgens(self):
        # The proxy event loop doesn't need to shut anything down; the
        # underlying event loop will shut down its own async generators.
        pass

    async def shutdown_default_executor(self, timeout=None):
        # The proxy event loop doesn't need to shut anything down; the
        # underlying event loop will shut down its own executor.
        pass

    def set_debug(self, enabled):
        # The proxy event loop doesn't need to manage debug, but `set_debug()` is a
        # required method on the loop.
        pass

    def is_closed(self):
        return self.closed

    def close(self):
        self.closed = True


@dataclass
class ProxyTask:
    coro: object
    kwargs: dict

    # Used by ensure_future.
    _source_traceback = None

    def done(self):
        return False
