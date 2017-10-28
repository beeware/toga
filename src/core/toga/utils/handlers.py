import asyncio
import inspect


@asyncio.coroutine
def long_running_task(generator):
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
        pass


def wrapped_handler(interface, handler):
    """Wrap a handler provided by the user so it can be invoked.

    If the handler is a bound method, or function, invoke it as it,
        and return the result.
    If the handler is a generator, invoke it asynchronously, with
        the yield values from the generator representing the duration
        to sleep between iterations.
    If the handler is a coroutine, install it on the asynchronous
        event loop.
    """
    if handler:
        def _handler(widget, **extra):
            if asyncio.iscoroutinefunction(handler):
                asyncio.async(handler(interface, **extra))
            else:
                result = handler(interface, **extra)
                if inspect.isgenerator(result):
                    asyncio.async(long_running_task(result))
                else:
                    return result
        _handler._raw = handler

        return _handler
