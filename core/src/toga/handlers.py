import asyncio
import inspect
import sys
import traceback
import warnings
from abc import ABC


class NativeHandler:
    def __init__(self, handler):
        self.native = handler


async def long_running_task(interface, generator, cleanup):
    """Run a generator as an asynchronous coroutine."""
    try:
        try:
            while True:
                delay = next(generator)
                if delay:
                    await asyncio.sleep(delay)
        except StopIteration as e:
            result = e.value
    except Exception as e:
        print("Error in long running handler:", e, file=sys.stderr)
        traceback.print_exc()
    else:
        if cleanup:
            try:
                cleanup(interface, result)
            except Exception as e:
                print("Error in long running handler cleanup:", e, file=sys.stderr)
                traceback.print_exc()


async def handler_with_cleanup(handler, cleanup, interface, *args, **kwargs):
    try:
        result = await handler(interface, *args, **kwargs)
    except Exception as e:
        print("Error in async handler:", e, file=sys.stderr)
        traceback.print_exc()
    else:
        if cleanup:
            try:
                cleanup(interface, result)
            except Exception as e:
                print("Error in async handler cleanup:", e, file=sys.stderr)
                traceback.print_exc()


def wrapped_handler(interface, handler, cleanup=None):
    """Wrap a handler provided by the user, so it can be invoked.

    If the handler is a NativeHandler, return the handler object contained in the
    NativeHandler.

    If the handler is a bound method, or function, invoke it as it, and return the
    result.

    If the handler is a generator, invoke it asynchronously, with the yield values from
    the generator representing the duration to sleep between iterations.

    If the handler is a coroutine, install it on the asynchronous event loop.

    Returns either the native handler, or a wrapped function that will invoke the
    handler, using the interface as context. If a non-native handler, the wrapper
    function is annotated with the original handler function on the `_raw` attribute.
    """
    if handler:
        if isinstance(handler, NativeHandler):
            return handler.native

        def _handler(*args, **kwargs):
            if asyncio.iscoroutinefunction(handler):
                asyncio.ensure_future(
                    handler_with_cleanup(handler, cleanup, interface, *args, **kwargs)
                )
            else:
                try:
                    result = handler(interface, *args, **kwargs)
                except Exception as e:
                    print("Error in handler:", e, file=sys.stderr)
                    traceback.print_exc()
                else:
                    if inspect.isgenerator(result):
                        asyncio.ensure_future(
                            long_running_task(interface, result, cleanup)
                        )
                    else:
                        try:
                            if cleanup:
                                cleanup(interface, result)
                            return result
                        except Exception as e:
                            print("Error in handler cleanup:", e, file=sys.stderr)
                            traceback.print_exc()

        _handler._raw = handler

    else:
        # A dummy no-op handler
        def _handler(*args, **kwargs):
            try:
                if cleanup:
                    cleanup(interface, None)
            except Exception as e:
                print("Error in handler cleanup:", e, file=sys.stderr)
                traceback.print_exc()

        _handler._raw = None

    return _handler


class AsyncResult(ABC):
    def __init__(self, on_result=None):
        loop = asyncio.get_event_loop()
        self.future = loop.create_future()

        ######################################################################
        # 2023-12: Backwards compatibility
        ######################################################################
        if on_result:
            warnings.warn(
                "Synchronous `on_result` handlers have been deprecated; use `await` on the asynchronous result",
                DeprecationWarning,
            )

            self.on_result = on_result
        else:
            self.on_result = None
        ######################################################################
        # End backwards compatibility.
        ######################################################################

    def set_result(self, result):
        if not self.future.cancelled():
            self.future.set_result(result)
            if self.on_result:
                self.on_result(result)

    def set_exception(self, exc):
        if not self.future.cancelled():
            self.future.set_exception(exc)
            if self.on_result:
                self.on_result(None, exception=exc)

    def __repr__(self):
        return f"<Async {self.RESULT_TYPE} result; future={self.future}>"

    def __await__(self):
        return self.future.__await__()

    # All the comparison dunder methods are disabled
    def __bool__(self, other):
        raise RuntimeError(
            f"Can't check {self.RESULT_TYPE} result directly; use await or an on_result handler"
        )

    __lt__ = __bool__
    __le__ = __bool__
    __eq__ = __bool__
    __ne__ = __bool__
    __gt__ = __bool__
    __ge__ = __bool__
