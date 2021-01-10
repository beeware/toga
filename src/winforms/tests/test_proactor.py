from toga_winforms.libs import proactor, WinForms
import unittest
import unittest.mock as mock
import asyncio
from threading import Thread


class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1


def wrapped_func(func, *args, **kwargs):
    def wrapper(func, *args, **kwargs):
        while True:
            func(*args)
    return wrapper


class TestProactor(unittest.TestCase):
    def setUp(self):
        self.loop = proactor.WinformsProactorEventLoop()
        # asyncio.set_event_loop(self.loop)
        self.app_context = WinForms.ApplicationContext()

    def test_proactor_loop(self):
        print("=====================================================================")
        # c = Counter()
        # with mock.patch.object(Counter, 'increment', wraps=c.increment) as fake_increment:
        func = wrapped_func(self.loop.run_forever, self.app_context)
        print("wrapped:", func)
        thread = Thread(target=func)
        thread.start()
        # await asyncio.sleep(5)
        print('Started!')
        self.loop.call_soon_threadsafe(self.loop.stop)  # here
        print('Requested stop!')
        thread.join()
        # self.loop.run_forever(self.app_context)
        print('Finished!')
        # print("fake_increment:", fake_increment)
        # unittest.TestCase.assertGreaterEqual(1, fake_increment.count)
