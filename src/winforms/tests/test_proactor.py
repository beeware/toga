from toga_winforms.libs import proactor, WinForms
import unittest
import unittest.mock as mock
import asyncio
from unittest import IsolatedAsyncioTestCase


class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1


def async_test(coro):
    def wrapper(*args, **kwargs):
        await coro
    return wrapper


class TestProactor(unittest.TestCase):

    @async_test
    async def test_proactor_loop(self):
        print("=====================================================================")
        c = Counter()
        with mock.patch.object(Counter, 'increment', wraps=c.increment) as fake_increment:
            self.loop = proactor.WinformsProactorEventLoop()
            asyncio.set_event_loop(self.loop)
            self.app_context = WinForms.ApplicationContext()
            self.loop.run_forever(self.app_context)
            await asyncio.sleep(5)
            self.loop.stop()
            unittest.TestCase.assertGreaterEqual(1, fake_increment.count)
