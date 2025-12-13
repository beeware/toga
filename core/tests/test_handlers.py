import asyncio
import gc
from unittest.mock import Mock

import pytest

from toga.handlers import (
    AsyncResult,
    NativeHandler,
    WeakrefCallable,
    simple_handler,
    wrapped_handler,
)


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
        "Error in handler cleanup: Problem in cleanup\n"
        "Traceback (most recent call last):\n" in capsys.readouterr().err
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
    cleanup.assert_called_once_with(obj, 42, "arg1", "arg2", kwarg1=3, kwarg2=4)


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
    cleanup.assert_called_once_with(obj, 42, "arg1", "arg2", kwarg1=3, kwarg2=4)

    # Evidence of the handler cleanup error is in the log.
    assert (
        "Error in handler cleanup: Problem in cleanup\n"
        "Traceback (most recent call last):\n" in capsys.readouterr().err
    )


######################################################################
# 2025-02: Generator handlers deprecated in 0.5.0
######################################################################


async def test_generator_handler():
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

    # Invoke the handler, and run until it is complete. Raises a deprecation warning.
    with pytest.warns(
        DeprecationWarning,
        match=r"Use of generators for async handlers has been deprecated;",
    ):
        assert await wrapped("arg1", "arg2", kwarg1=3, kwarg2=4) == 42

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
        "slept": True,
        "done": True,
    }


async def test_generator_handler_error(capsys):
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

    # Invoke the handler; raises a deprecation warning, return value is None due to
    # exception.
    with pytest.warns(
        DeprecationWarning,
        match=r"Use of generators for async handlers has been deprecated;",
    ):
        assert await wrapped("arg1", "arg2", kwarg1=3, kwarg2=4) is None

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
    }

    # Evidence of the handler cleanup error is in the log.
    assert (
        "Error in long running handler: Problem in handler\n"
        "Traceback (most recent call last):\n" in capsys.readouterr().err
    )


async def test_generator_handler_with_cleanup():
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

    # Invoke the handler; raises a deprecation warning
    with pytest.warns(
        DeprecationWarning,
        match=r"Use of generators for async handlers has been deprecated;",
    ):
        assert await wrapped("arg1", "arg2", kwarg1=3, kwarg2=4) == 42

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
        "slept": True,
        "done": True,
    }

    # Cleanup method was invoked
    cleanup.assert_called_once_with(obj, 42)


async def test_generator_handler_with_cleanup_error(capsys):
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

    # Invoke the handler; raises a deprecation warning, error in cleanup is swallowed
    with pytest.warns(
        DeprecationWarning,
        match=r"Use of generators for async handlers has been deprecated;",
    ):
        assert await wrapped("arg1", "arg2", kwarg1=3, kwarg2=4) == 42

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
        "Error in long running handler cleanup: Problem in cleanup\n"
        "Traceback (most recent call last):\n" in capsys.readouterr().err
    )


######################################################################


async def test_coroutine_handler():
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
    assert await wrapped("arg1", "arg2", kwarg1=3, kwarg2=4) == 42

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
        "done": True,
    }


async def test_coroutine_handler_error(capsys):
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
    assert await wrapped("arg1", "arg2", kwarg1=3, kwarg2=4) is None

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
    }

    # Evidence of the handler cleanup error is in the log.
    assert (
        "Error in async handler: Problem in handler\n"
        "Traceback (most recent call last):\n" in capsys.readouterr().err
    )


async def test_coroutine_handler_with_cleanup():
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
    assert await wrapped("arg1", "arg2", kwarg1=3, kwarg2=4) == 42

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
        "done": True,
    }

    # Cleanup method was invoked
    cleanup.assert_called_once_with(obj, 42, "arg1", "arg2", kwarg1=3, kwarg2=4)


async def test_coroutine_handler_with_cleanup_error(capsys):
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
    assert await wrapped("arg1", "arg2", kwarg1=3, kwarg2=4) == 42

    # Handler arguments are as expected.
    assert handler_call == {
        "args": (obj, "arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
        "done": True,
    }

    # Cleanup method was invoked
    cleanup.assert_called_once_with(obj, 42, "arg1", "arg2", kwarg1=3, kwarg2=4)

    # Evidence of the handler cleanup error is in the log.
    assert (
        "Error in async handler cleanup: Problem in cleanup\n"
        "Traceback (most recent call last):\n" in capsys.readouterr().err
    )


def test_native_handler():
    """A native function can be used as a handler."""
    obj = Mock()
    native_method = Mock()

    handler = NativeHandler(native_method)

    wrapped = wrapped_handler(obj, handler)

    # Native method is returned as the handler.
    assert wrapped == native_method


async def test_async_result_non_comparable():
    """An async result can't be compared or evaluated."""
    result = ExampleAsyncResult(None)

    # repr for the result is useful
    assert repr(result).startswith("<Async Test result; future=<Future pending")

    # Result cannot be compared.

    with pytest.raises(
        RuntimeError,
        match=r"Can't check Test result directly; use await or an on_result handler",
    ):
        _ = result == 42

    with pytest.raises(
        RuntimeError,
        match=r"Can't check Test result directly; use await or an on_result handler",
    ):
        _ = result < 42

    with pytest.raises(
        RuntimeError,
        match=r"Can't check Test result directly; use await or an on_result handler",
    ):
        _ = result <= 42

    with pytest.raises(
        RuntimeError,
        match=r"Can't check Test result directly; use await or an on_result handler",
    ):
        _ = result > 42

    with pytest.raises(
        RuntimeError,
        match=r"Can't check Test result directly; use await or an on_result handler",
    ):
        _ = result >= 42

    with pytest.raises(
        RuntimeError,
        match=r"Can't check Test result directly; use await or an on_result handler",
    ):
        _ = result != 42


async def test_async_result():
    """An async result can be set."""
    result = ExampleAsyncResult()

    result.set_result(42)

    # Evaluate the future
    async_answer = await result.future

    # The answer was returned, and passed to the callback
    assert async_answer == 42


async def test_async_result_cancelled():
    """An async result can be set even if the future is cancelled."""
    result = ExampleAsyncResult()

    # cancel the future.
    result.future.cancel()

    result.set_result(42)

    # Evaluate the future. This will raise an error
    with pytest.raises(asyncio.CancelledError):
        await result.future


async def test_async_exception():
    """An async result can raise an exception."""
    result = ExampleAsyncResult()

    result.set_exception(ValueError("Bad stuff"))

    # Evaluate the future; this will raise an exception
    with pytest.raises(ValueError, match=r"Bad stuff"):
        await result.future


async def test_async_exception_cancelled():
    """An async result can raise an exception even if the future is cancelled."""
    result = ExampleAsyncResult()

    # Cancel the future
    result.future.cancel()

    result.set_exception(ValueError("Bad stuff"))

    # Evaluate the future. This will raise an error
    with pytest.raises(asyncio.CancelledError):
        await result.future


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


async def test_simple_handler_coroutine():
    """A coroutine can be wrapped as a simple handler."""
    handler_call = {}

    async def handler(*args, **kwargs):
        handler_call["args"] = args
        handler_call["kwargs"] = kwargs
        return 42

    wrapped = simple_handler(handler, "arg1", "arg2", kwarg1=3, kwarg2=4)

    # Invoke the handler as if it were a coroutine method handler (i.e., with the extra
    # "widget" argument)
    assert await wrapped("obj") == 42
    assert wrapped._raw == handler

    # The "widget" bound argument has been dropped
    assert handler_call == {
        "args": ("arg1", "arg2"),
        "kwargs": {"kwarg1": 3, "kwarg2": 4},
    }


######################################################################
# 2023-12: Backwards compatibility for <= 0.4.0
######################################################################


async def test_async_result_sync():
    """The deprecated behavior of using a synchronous result handler is supported."""
    on_result = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        result = ExampleAsyncResult(on_result)

    result.set_result(42)

    # Evaluate the future
    async_answer = await result.future

    # The answer was returned, and passed to the callback
    assert async_answer == 42
    on_result.assert_called_once_with(42)


async def test_async_result_cancelled_sync():
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
        await result.future

    # The callback wasn't called
    on_result.assert_not_called()


async def test_async_exception_sync():
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
        await result.future

    # The answer was returned, and passed to the callback
    on_result.assert_called_once()
    assert on_result.call_args[0] == (None,)
    assert isinstance(on_result.call_args[1]["exception"], ValueError)


async def test_async_exception_cancelled_sync():
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
        await result.future

    # The callback wasn't called
    on_result.assert_not_called()


def test_weakref_function_call():
    """WeakrefCallable correctly calls the wrapped function."""

    def test_func(x, y=2):
        return x + y

    wrc = WeakrefCallable(test_func)

    # Test with positional arguments
    assert wrc(3) == 5

    # Test with keyword arguments
    assert wrc(3, y=3) == 6

    # Test with mixed arguments
    assert wrc(3, 4) == 7


def test_weakref_method_call():
    """WeakrefCallable correctly calls a method."""

    class TestClass:
        def __init__(self, value):
            self.value = value

        def method(self, x, y=2):
            return self.value + x + y

    obj = TestClass(5)
    wrc = WeakrefCallable(obj.method)

    # Test method call
    assert wrc(3) == 10

    # Test with keyword arguments
    assert wrc(3, y=3) == 11

    # Test with mixed arguments
    assert wrc(3, 4) == 12


def test_weakref_lambda_call():
    """WeakrefCallable works with lambda functions."""
    # Store the lambda in a variable to prevent it from being garbage collected
    lambda_func = lambda x: x * 2  # noqa: E731
    wrc = WeakrefCallable(lambda_func)
    assert wrc(5) == 10


def test_weakref_gc_function():
    """A function is garbage collected properly."""

    def create_function_wrapper():
        def temp_func(x):
            return x * 3

        return WeakrefCallable(temp_func)

    wrc = create_function_wrapper()

    # Force garbage collection
    gc.collect()

    # The function should be gone
    assert wrc.ref() is None


def test_weakref_gc_method():
    """The method and its object are garbage collected properly."""

    class TempClass:
        def method(self, x):
            return x * 4

    def create_method_wrapper():
        obj = TempClass()
        return WeakrefCallable(obj.method), obj

    wrc, obj_ref = create_method_wrapper()

    # Object still exists, method should work
    assert wrc(2) == 8

    # Delete the reference to the object
    del obj_ref

    # Force garbage collection
    gc.collect()

    # The method reference should be gone
    assert wrc.ref() is None


def test_weakref_callable_object():
    """WeakrefCallable works with callable objects."""

    class CallableObject:
        def __call__(self, x):
            return x * 5

    obj = CallableObject()
    wrc = WeakrefCallable(obj)

    # Test call
    assert wrc(2) == 10


def test_weakref_none_result_when_function_gone():
    """Calling the wrapper after the target is collected doesn't error."""

    def create_function_wrapper():
        def temp_func(x):
            return x * 3

        return WeakrefCallable(temp_func)

    wrc = create_function_wrapper()

    # Force garbage collection
    gc.collect()

    # Calling the wrapper should not raise an error
    result = wrc(10)
    assert result is None
