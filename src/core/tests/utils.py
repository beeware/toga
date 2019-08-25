import asyncio


def async_test(coroutine):
    """Run an async test to completion."""
    def _test(self):
        asyncio.get_event_loop().run_until_complete(coroutine(self))

    return _test
