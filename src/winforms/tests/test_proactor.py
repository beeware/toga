from toga_dummy.utils import TestCase
from toga_winforms import proactor
import unittest


class TestWindow(TestCase):
    def setUp(self):
        super().setUp()

    def test_proactor_loop(self):
        self.proactor = proactor.WinformsProactorEventLoop().run_forever(None)
