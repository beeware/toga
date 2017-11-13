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

    Returns a wrapped function that will invoke the handler, using
    the interface as context. The wrapper function is annotated with
    the original handler function on the `_raw` attribute.
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


def wrapped_canvas_handler(interface, handler):
    """Wrap a handler and add canvas and context arguments
    """
    if handler:
        def _handler(canvas, context, **extra):
            interface.factory.Canvas(interface=interface).set_context = context
            if asyncio.iscoroutinefunction(handler):
                asyncio.async(handler(interface, **extra))
            else:
                # TODO we need to avoid calling the handler before establishing the native on_draw handler
                # result = handler(interface, **extra)
                # if inspect.isgenerator(result):
                #     asyncio.async(long_running_task(result))
                # else:
                return handler
        _handler._raw = handler
        return _handler
