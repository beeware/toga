from toga_dummy.utils import TestCase
from toga_winforms.libs import proactor, WinForms
import unittest
import unittest.mock as mock
import asyncio


class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1


def async_test(f):
    def wrapper(*args, **kwargs):
        coro = asyncio.coroutine(f)
        future = coro(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper


class TestWindow(TestCase):
    def setUp(self):
        super().setUp()

    @async_test
    def test_proactor_loop(self):
        print("=====================================================================")
        c = Counter()
        with mock.patch.object(Counter, 'increment', wraps=c.increment) as fake_increment:
            self.loop = proactor.WinformsProactorEventLoop()
            asyncio.set_event_loop(self.loop)
            self.app_context = WinForms.ApplicationContext()
            self.loop.run_forever(self.app_context)
            unittest.TestCase.assertGreaterEqual(1, fake_increment.count)
