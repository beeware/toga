from toga_dummy.utils import TestCase
from toga_winforms.libs import proactor, WinForms
import unittest
import unittest.mock


class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

class TestWindow(TestCase):
    def setUp(self):
        super().setUp()

    def test_proactor_loop(self):
        print("=====================================================================")
        c = Counter()
        with mock.patch.object(Counter, 'increment', wraps=c.increment) as fake_increment:
            self.proactor = proactor.WinformsProactorEventLoop().run_forever(WinForms.ApplicationContext())
            unittest.TestCase.assertGreaterEqual(1, fake_increment.count)
