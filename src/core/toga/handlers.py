import asyncio
import inspect
import sys
import traceback


@asyncio.coroutine
def long_running_task(generator, cleanup):
    """Run a generator as an asynchronous coroutine

    When we drop Python 3.4 support, we can:
    * drop the decorator,
    * rename the method as `async def`
    * change from `yield from` to `await`
    """
    try:
        while True:
            delay = next(generator)
            yield from asyncio.sleep(delay)
    except StopIteration:
        if cleanup:
            cleanup()
    except Exception as e:
        print('Error in long running handler:', e, file=sys.stderr)
        traceback.print_exc()


@asyncio.coroutine
def handler_with_cleanup(handler, cleanup, interface, **extra):
    try:
        yield from handler(interface, **extra)
        if cleanup:
            cleanup()
    except Exception as e:
        print('Error in async handler:', e, file=sys.stderr)
        traceback.print_exc()


def wrapped_handler(interface, handler, cleanup=None):
    """Wrap a handler provided by the user so it can be invoked.

    If the handler is a bound method, or function, invoke it as it,
        and return the result.
    If the handler is a generator, invoke it asynchronously, with
        the yield values from the generator representing the duration
        to sleep between iterations.
    If the handler is a coroutine, install it on the asynchronous
        event loop.

    Returns a wrapped function that will invoke the handler, using
    the interface as context. The wrapper function is annotated with
    the original handler function on the `_raw` attribute.
    """
    if handler:
        def _handler(widget, **extra):
            if asyncio.iscoroutinefunction(handler):
                asyncio.ensure_future(
                    handler_with_cleanup(handler, cleanup, interface, **extra)
                )
            else:
                result = handler(interface, **extra)
                if inspect.isgenerator(result):
                    asyncio.ensure_future(
                        long_running_task(result, cleanup)
                    )
                else:
                    try:
                        if cleanup:
                            cleanup()
                        return result
                    except Exception as e:
                        print('Error in handler:', e, file=sys.stderr)
                        traceback.print_exc()

        _handler._raw = handler

        return _handler
