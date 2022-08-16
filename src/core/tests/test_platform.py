from toga.platform import get_platform_factory, default_factory
import toga_dummy
from toga_dummy.utils import TestCase


class NumberInputTests(TestCase):
    def setUp(self):
        super().setUp()

    def test_get_platform_factory(self):
        factory = get_platform_factory()
        self.assertIsNotNone(factory)
        self.assertIsNotNone(factory.App)

    def test_get_platform_factory_defined(self):
        factory = get_platform_factory(factory=toga_dummy.factory)
        self.assertEquals(factory, toga_dummy.factory)

    def test_default_platform(self):
        default_factory(toga_dummy.factory)
        factory = get_platform_factory()
        self.assertEquals(factory, toga_dummy.factory)
        default_factory(None)
        factory = get_platform_factory()
        self.assertIsNotNone(factory)
        self.assertNotEquals(factory, toga_dummy.factory)
