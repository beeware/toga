import asyncio
import inspect
from dataclasses import dataclass

from pytest import fixture, register_assert_rewrite, skip

import toga

# Ideally, we'd register rewrites for "tests" and get all the submodules
# recursively; however we've already imported "tests", so that raises a warning.
register_assert_rewrite("tests.assertions")
register_assert_rewrite("tests.widgets")
register_assert_rewrite("tests_backend")


def skip_on_platforms(*platforms):
    current_platform = toga.platform.current_platform
    if current_platform in platforms:
        skip(f"not applicable on {current_platform}")


@fixture(scope="session")
def app():
    return toga.App.app


@fixture(scope="session")
def main_window(app):
    return app.main_window


# Controls the event loop used by pytest-asyncio.
@fixture(scope="session")
def event_loop(app):
    return ProxyEventLoop(app._impl.loop)


# Proxy which forwards all tasks to another event loop in a thread-safe manner. It
# implements only the methods used by pytest-asyncio.
@dataclass
class ProxyEventLoop(asyncio.AbstractEventLoop):
    loop: object

    # Used by ensure_future.
    def create_task(self, coro):
        return ProxyTask(coro)

    def run_until_complete(self, future):
        if inspect.iscoroutine(future):
            coro = future
        elif isinstance(future, ProxyTask):
            coro = future.coro
        else:
            raise TypeError(f"Future type {type(future)} is not currently supported")
        return asyncio.run_coroutine_threadsafe(coro, self.loop).result()

    def close(self):
        pass


@dataclass
class ProxyTask:
    coro: object

    # Used by ensure_future.
    _source_traceback = None

    def done(self):
        return False
