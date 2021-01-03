import unittest
from toga import handlers
from .utils import async_test
import time
import inspect


def generator(iface, obj):
    for i in range(5):
        obj.var = i
        yield 1


async def handler(interface, obj):
    obj.var = 'b'


class HandlerTests(unittest.TestCase):

    @async_test
    async def test_long_running_task(self):
        self.var = None
        start = time.time()
        res = generator(None, self)
        await handlers.long_running_task(res, None)
        end = time.time()
        self.assertGreaterEqual(end - start, 5)
        self.assertEqual(self.var, 4)

    @async_test
    async def test_handler_with_cleanup(self):
        self.var = None
        await handlers.handler_with_cleanup(handler, None, None, self)
        self.assertEqual(self.var, 'b')

#     @async_test
#     async def test_wrapped_handler(self):
#         print("=====================================================")
#         self.var = None
#         w_handle = handlers.wrapped_handler(None, generator)
#         print(w_handle(None, self))
#         self.assertEqual(self.var, 4)
