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


def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = coro
        thread = Thread(target=coro.loop.run_forever)
        thread.start()
        print('Started!')
        loop.call_soon_threadsafe(loop.stop)  # here
        print('Requested stop!')
        thread.join()
        print('Finished!')
    return wrapper


class TestProactor(unittest.TestCase):

    @async_test
    async def test_proactor_loop(self):
        print("=====================================================================")
        c = Counter()
        with mock.patch.object(Counter, 'increment', wraps=c.increment) as fake_increment:
            loop = proactor.WinformsProactorEventLoop()
            asyncio.set_event_loop(loop)
            self.app_context = WinForms.ApplicationContext()
            loop.run_forever(self.app_context)
            await asyncio.sleep(5)
            loop.stop()
            unittest.TestCase.assertGreaterEqual(1, fake_increment.count)
