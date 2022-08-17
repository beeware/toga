from toga.platform import get_platform_factory, default_factory
import toga_dummy
from toga_dummy.utils import TestCase


class PlatformTests(TestCase):
    def setUp(self):
        # We can't test the default behaviour of ``get_platform_factory()`` in CI:
        # the CI environment is only installing toga_core and toga_dummy.
        # This test must be done before the call to super().setUp(), which will set
        # the default_factory.
        try:
            get_platform_factory()
            self.native_platform_factory_available = True
        except ModuleNotFoundError:
            self.native_platform_factory_available = False

        super().setUp()

    def test_get_platform_factory(self):
        if self.native_platform_factory_available:
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

        if self.native_platform_factory_available:
            factory = get_platform_factory()
            self.assertIsNotNone(factory)
            self.assertNotEquals(factory, toga_dummy.factory)
        else:
            with self.assertRaises(ModuleNotFoundError):
                get_platform_factory()
