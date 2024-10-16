import asyncio
from unittest.mock import Mock

import pytest

from toga.handlers import AsyncResult, NativeHandler, simple_handler, wrapped_handler


class ExampleAsyncResult(AsyncResult):
    RESULT_TYPE = "Test"


def test_noop_handler():
    """None can be wrapped as a valid handler."""
    obj = Mock()

    wrapped = wrapped_handler(obj, None)

    assert wrapped._raw is None

    # This does nothing, but doesn't raise an error, and returns None
    assert wrapped("arg1", "arg2", kwarg1=3, kwarg2=4) is None


def test_noop_handler_with_cleanup():
    """Cleanup is still performed when a no-op handler is used."""
    obj = Mock()
    cleanup = Mock()

    wrapped = wrapped_handler(obj, None, cleanup=cleanup)

    assert wrapped._raw is None

    # This does nothing, but doesn't raise an error, and returns None
    assert wrapped("arg1", "arg2", kwarg1=3, kwarg2=4) is None

    # Cleanup method was invoked
    cleanup.assert_called_once_with(obj, None)


def test_noop_handler_with_cleanup_error(capsys):
    """If cleanup on a no-op handler raises an error, it is logged."""
    obj = Mock()
    cleanup = Mock(side_effect=Exception("Problem in cleanup"))

    wrapped = wrapped_handler(obj, None, cleanup=cleanup)

    assert wrapped._raw is None

    # This does nothing, but doesn't raise an error, and returns None
    assert wrapped("arg1", "arg2", kwarg1=3, kwarg2=4) is None

    # Cleanup method was invoked
    cleanup.assert_called_once_with(obj, None)

    # Evidence of the handler cleanup error is in the log.
    assert (
        "Error in handler cleanup: Problem in cleanup\nTraceback (most recent call last):\n"
        in capsys.readouterr().err
    )


def test_function_handler():
    """A function can be used as a handler."""
    obj = Mock()
    handler_call = {}

    def handler(*args, **kwargs):
        handler_call["args"] = args
        handler_call["kwargs"] = kwargs
        return 42

    wrapped = wrapped_handler(obj, handler)

    # Raw handler is the original function
    assert wrapped._raw == handler

    # Invoke wrapper; handler return value is preserved
    assert wrapped("arg1", "arg2", kwarg1=3, kwarg2=4) == 42

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
    }


def test_function_handler_error(capsys):
    """A function handler can raise an error."""
    obj = Mock()
    handler_call = {}

    def handler(*args, **kwargs):
        handler_call["args"] = args
        handler_call["kwargs"] = kwargs
        raise Exception("Problem in handler")

    wrapped = wrapped_handler(obj, handler)

    assert wrapped._raw == handler

    # Invoke handler. The exception is swallowed; return value is None
    assert wrapped("arg1", "arg2", kwarg1=3, kwarg2=4) is None

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
    }

    # Evidence of the handler error is in the log.
    assert (
        "Error in handler: Problem in handler\nTraceback (most recent call last):\n"
        in capsys.readouterr().err
    )


def test_function_handler_with_cleanup():
    """A function handler can have a cleanup method."""
    obj = Mock()
    cleanup = Mock()
    handler_call = {}

    def handler(*args, **kwargs):
        handler_call["args"] = args
        handler_call["kwargs"] = kwargs
        return 42

    wrapped = wrapped_handler(obj, handler, cleanup=cleanup)

    # Raw handler is the original function
    assert wrapped._raw == handler

    # Invoke handler
    assert wrapped("arg1", "arg2", kwarg1=3, kwarg2=4) == 42

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
    }

    # Cleanup method was invoked
    cleanup.assert_called_once_with(obj, 42)


def test_function_handler_with_cleanup_error(capsys):
    """A function handler can have a cleanup method that raises an error."""
    obj = Mock()
    cleanup = Mock(side_effect=Exception("Problem in cleanup"))
    handler_call = {}

    def handler(*args, **kwargs):
        handler_call["args"] = args
        handler_call["kwargs"] = kwargs
        return 42

    wrapped = wrapped_handler(obj, handler, cleanup=cleanup)

    # Raw handler is the original function
    assert wrapped._raw == handler

    # Invoke handler. The error in cleanup is swallowed.
    assert wrapped("arg1", "arg2", kwarg1=3, kwarg2=4) == 42

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
    }

    # Cleanup method was invoked
    cleanup.assert_called_once_with(obj, 42)

    # Evidence of the handler cleanup error is in the log.
    assert (
        "Error in handler cleanup: Problem in cleanup\nTraceback (most recent call last):\n"
        in capsys.readouterr().err
    )


def test_generator_handler(event_loop):
    """A generator can be used as a handler."""
    obj = Mock()
    handler_call = {}

    def handler(*args, **kwargs):
        handler_call["args"] = args
        handler_call["kwargs"] = kwargs
        yield 0.01  # A short sleep
        handler_call["slept"] = True
        yield  # A yield without a sleep
        handler_call["done"] = True
        return 42

    wrapped = wrapped_handler(obj, handler)

    # Raw handler is the original generator
    assert wrapped._raw == handler

    # Invoke the handler, and run until it is complete.
    assert (
        event_loop.run_until_complete(wrapped("arg1", "arg2", kwarg1=3, kwarg2=4)) == 42
    )

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
        "slept": True,
        "done": True,
    }


def test_generator_handler_error(event_loop, capsys):
    """A generator can raise an error."""
    obj = Mock()
    handler_call = {}

    def handler(*args, **kwargs):
        handler_call["args"] = args
        handler_call["kwargs"] = kwargs
        yield 0.01  # A short sleep
        raise Exception("Problem in handler")

    wrapped = wrapped_handler(obj, handler)

    # Raw handler is the original generator
    assert wrapped._raw == handler

    # Invoke the handler; return value is None due to exception
    assert (
        event_loop.run_until_complete(wrapped("arg1", "arg2", kwarg1=3, kwarg2=4))
        is None
    )

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
    }

    # Evidence of the handler cleanup error is in the log.
    assert (
        "Error in long running handler: Problem in handler\nTraceback (most recent call last):\n"
        in capsys.readouterr().err
    )


def test_generator_handler_with_cleanup(event_loop):
    """A generator can have cleanup."""
    obj = Mock()
    cleanup = Mock()
    handler_call = {}

    def handler(*args, **kwargs):
        handler_call["args"] = args
        handler_call["kwargs"] = kwargs
        yield 0.01  # A short sleep
        handler_call["slept"] = True
        yield  # A yield without a sleep
        handler_call["done"] = True
        return 42

    wrapped = wrapped_handler(obj, handler, cleanup=cleanup)

    # Raw handler is the original generator
    assert wrapped._raw == handler

    # Invoke the handler
    assert (
        event_loop.run_until_complete(wrapped("arg1", "arg2", kwarg1=3, kwarg2=4)) == 42
    )

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
        "slept": True,
        "done": True,
    }

    # Cleanup method was invoked
    cleanup.assert_called_once_with(obj, 42)


def test_generator_handler_with_cleanup_error(event_loop, capsys):
    """A generator can raise an error during cleanup."""
    obj = Mock()
    cleanup = Mock(side_effect=Exception("Problem in cleanup"))
    handler_call = {}

    def handler(*args, **kwargs):
        handler_call["args"] = args
        handler_call["kwargs"] = kwargs
        yield 0.01  # A short sleep
        handler_call["slept"] = True
        yield  # A yield without a sleep
        handler_call["done"] = True
        return 42

    wrapped = wrapped_handler(obj, handler, cleanup=cleanup)

    # Raw handler is the original generator
    assert wrapped._raw == handler

    # Invoke the handler; error in cleanup is swallowed
    assert (
        event_loop.run_until_complete(wrapped("arg1", "arg2", kwarg1=3, kwarg2=4)) == 42
    )

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
        "slept": True,
        "done": True,
    }

    # Cleanup method was invoked
    cleanup.assert_called_once_with(obj, 42)

    # Evidence of the handler cleanup error is in the log.
    assert (
        "Error in long running handler cleanup: Problem in cleanup\nTraceback (most recent call last):\n"
        in capsys.readouterr().err
    )


def test_coroutine_handler(event_loop):
    """A coroutine can be used as a handler."""
    obj = Mock()
    handler_call = {}

    async def handler(*args, **kwargs):
        handler_call["args"] = args
        handler_call["kwargs"] = kwargs
        await asyncio.sleep(0.01)  # A short sleep
        handler_call["done"] = True
        return 42

    wrapped = wrapped_handler(obj, handler)

    # Raw handler is the original coroutine
    assert wrapped._raw == handler

    # Invoke the handler
    assert (
        event_loop.run_until_complete(wrapped("arg1", "arg2", kwarg1=3, kwarg2=4)) == 42
    )

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
        "done": True,
    }


def test_coroutine_handler_error(event_loop, capsys):
    """A coroutine can raise an error."""
    obj = Mock()
    handler_call = {}

    async def handler(*args, **kwargs):
        handler_call["args"] = args
        handler_call["kwargs"] = kwargs
        await asyncio.sleep(0.01)  # A short sleep
        raise Exception("Problem in handler")

    wrapped = wrapped_handler(obj, handler)

    # Raw handler is the original coroutine
    assert wrapped._raw == handler

    # Invoke the handler; return value is None due to exception
    assert (
        event_loop.run_until_complete(wrapped("arg1", "arg2", kwarg1=3, kwarg2=4))
        is None
    )

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
    }

    # Evidence of the handler cleanup error is in the log.
    assert (
        "Error in async handler: Problem in handler\nTraceback (most recent call last):\n"
        in capsys.readouterr().err
    )


def test_coroutine_handler_with_cleanup(event_loop):
    """A coroutine can have cleanup."""
    obj = Mock()
    cleanup = Mock()
    handler_call = {}

    async def handler(*args, **kwargs):
        handler_call["args"] = args
        handler_call["kwargs"] = kwargs
        await asyncio.sleep(0.01)  # A short sleep
        handler_call["done"] = True
        return 42

    wrapped = wrapped_handler(obj, handler, cleanup=cleanup)

    # Raw handler is the original coroutine
    assert wrapped._raw == handler

    # Invoke the handler
    assert (
        event_loop.run_until_complete(wrapped("arg1", "arg2", kwarg1=3, kwarg2=4)) == 42
    )

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
        "done": True,
    }

    # Cleanup method was invoked
    cleanup.assert_called_once_with(obj, 42)


def test_coroutine_handler_with_cleanup_error(event_loop, capsys):
    """A coroutine can raise an error during cleanup."""
    obj = Mock()
    cleanup = Mock(side_effect=Exception("Problem in cleanup"))
    handler_call = {}

    async def handler(*args, **kwargs):
        handler_call["args"] = args
        handler_call["kwargs"] = kwargs
        await asyncio.sleep(0.01)  # A short sleep
        handler_call["done"] = True
        return 42

    wrapped = wrapped_handler(obj, handler, cleanup=cleanup)

    # Raw handler is the original coroutine
    assert wrapped._raw == handler

    # Invoke the handler; error in cleanup is swallowed
    assert (
        event_loop.run_until_complete(wrapped("arg1", "arg2", kwarg1=3, kwarg2=4)) == 42
    )

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
        "done": True,
    }

    # Cleanup method was invoked
    cleanup.assert_called_once_with(obj, 42)

    # Evidence of the handler cleanup error is in the log.
    assert (
        "Error in async handler cleanup: Problem in cleanup\nTraceback (most recent call last):\n"
        in capsys.readouterr().err
    )


def test_native_handler():
    """A native function can be used as a handler."""
    obj = Mock()
    native_method = Mock()

    handler = NativeHandler(native_method)

    wrapped = wrapped_handler(obj, handler)

    # Native method is returned as the handler.
    assert wrapped == native_method


def test_async_result_non_comparable(event_loop):
    """An async result can't be compared or evaluated."""
    result = ExampleAsyncResult(None)

    # repr for the result is useful
    assert repr(result).startswith("<Async Test result; future=<Future pending")

    # Result cannot be compared.

    with pytest.raises(
        RuntimeError,
        match=r"Can't check Test result directly; use await or an on_result handler",
    ):
        result == 42

    with pytest.raises(
        RuntimeError,
        match=r"Can't check Test result directly; use await or an on_result handler",
    ):
        result < 42

    with pytest.raises(
        RuntimeError,
        match=r"Can't check Test result directly; use await or an on_result handler",
    ):
        result <= 42

    with pytest.raises(
        RuntimeError,
        match=r"Can't check Test result directly; use await or an on_result handler",
    ):
        result > 42

    with pytest.raises(
        RuntimeError,
        match=r"Can't check Test result directly; use await or an on_result handler",
    ):
        result >= 42

    with pytest.raises(
        RuntimeError,
        match=r"Can't check Test result directly; use await or an on_result handler",
    ):
        result != 42


def test_async_result(event_loop):
    """An async result can be set."""
    result = ExampleAsyncResult()

    result.set_result(42)

    # Evaluate the future
    async_answer = event_loop.run_until_complete(result.future)

    # The answer was returned, and passed to the callback
    assert async_answer == 42


def test_async_result_cancelled(event_loop):
    """An async result can be set even if the future is cancelled."""
    result = ExampleAsyncResult()

    # cancel the future.
    result.future.cancel()

    result.set_result(42)

    # Evaluate the future. This will raise an error
    with pytest.raises(asyncio.CancelledError):
        event_loop.run_until_complete(result.future)


def test_async_exception(event_loop):
    """An async result can raise an exception."""
    result = ExampleAsyncResult()

    result.set_exception(ValueError("Bad stuff"))

    # Evaluate the future; this will raise an exception
    with pytest.raises(ValueError, match=r"Bad stuff"):
        event_loop.run_until_complete(result.future)


def test_async_exception_cancelled(event_loop):
    """An async result can raise an exception even if the future is cancelled."""
    result = ExampleAsyncResult()

    # Cancel the future
    result.future.cancel()

    result.set_exception(ValueError("Bad stuff"))

    # Evaluate the future. This will raise an error
    with pytest.raises(asyncio.CancelledError):
        event_loop.run_until_complete(result.future)


def test_simple_handler_function():
    """A function can be wrapped as a simple handler."""
    handler_call = {}

    def handler(*args, **kwargs):
        handler_call["args"] = args
        handler_call["kwargs"] = kwargs
        return 42

    wrapped = simple_handler(handler, "arg1", "arg2", kwarg1=3, kwarg2=4)

    # Invoke the handler as if it were a method handler (i.e., with the extra "widget"
    # argument)
    assert wrapped("obj") == 42
    assert wrapped._raw == handler

    # The "widget" bound argument has been dropped
    assert handler_call == {
        "args": ("arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
    }


def test_simple_handler_coroutine(event_loop):
    """A coroutine can be wrapped as a simple handler."""
    handler_call = {}

    async def handler(*args, **kwargs):
        handler_call["args"] = args
        handler_call["kwargs"] = kwargs
        return 42

    wrapped = simple_handler(handler, "arg1", "arg2", kwarg1=3, kwarg2=4)

    # Invoke the handler as if it were a coroutine method handler (i.e., with the extra
    # "widget" argument)
    assert event_loop.run_until_complete(wrapped("obj")) == 42
    assert wrapped._raw == handler

    # The "widget" bound argument has been dropped
    assert handler_call == {
        "args": ("arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
    }


######################################################################
# 2023-12: Backwards compatibility
######################################################################


def test_async_result_sync(event_loop):
    """The deprecated behavior of using a synchronous result handler is supported."""
    on_result = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        result = ExampleAsyncResult(on_result)

    result.set_result(42)

    # Evaluate the future
    async_answer = event_loop.run_until_complete(result.future)

    # The answer was returned, and passed to the callback
    assert async_answer == 42
    on_result.assert_called_once_with(42)


def test_async_result_cancelled_sync(event_loop):
    """A deprecated on_result handler won't be fired on a cancelled future."""
    on_result = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        result = ExampleAsyncResult(on_result)

    # cancel the future.
    result.future.cancel()

    result.set_result(42)

    # Evaluate the future. This will raise an error
    with pytest.raises(asyncio.CancelledError):
        event_loop.run_until_complete(result.future)

    # The callback wasn't called
    on_result.assert_not_called()


def test_async_exception_sync(event_loop):
    """A deprecated on_result handler can raise an exception."""
    on_result = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        result = ExampleAsyncResult(on_result)

    result.set_exception(ValueError("Bad stuff"))

    # Evaluate the future; this will raise an exception
    with pytest.raises(ValueError, match=r"Bad stuff"):
        event_loop.run_until_complete(result.future)

    # The answer was returned, and passed to the callback
    on_result.assert_called_once()
    assert on_result.call_args[0] == (None,)
    assert isinstance(on_result.call_args[1]["exception"], ValueError)


def test_async_exception_cancelled_sync(event_loop):
    """An async result can raise an exception even if the future is cancelled."""
    on_result = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        result = ExampleAsyncResult(on_result)

    # Cancel the future
    result.future.cancel()

    result.set_exception(ValueError("Bad stuff"))

    # Evaluate the future. This will raise an error
    with pytest.raises(asyncio.CancelledError):
        event_loop.run_until_complete(result.future)

    # The callback wasn't called
    on_result.assert_not_called()
