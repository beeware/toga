from toga_dummy.utils import TestCase
from toga_winforms.libs import proactor, WinForms
import unittest


class TestWindow(TestCase):
    def setUp(self):
        super().setUp()

    def test_proactor_loop(self):
        self.proactor = proactor.WinformsProactorEventLoop().run_forever(WinForms.ApplicationContext())
