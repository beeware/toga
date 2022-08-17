from toga.platform import get_platform_factory, default_factory
import toga_dummy
from toga_dummy.utils import TestCase


# We can't test the default behaviour of ``get_platform_factory()`` in CI:
# the CI environment only installs toga_core and toga_dummy.
try:
    get_platform_factory()
    native_platform_factory_available = True
except ModuleNotFoundError:
    native_platform_factory_available = False


class PlatformTests(TestCase):

    def test_get_platform_factory(self):
        if not native_platform_factory_available:
            self.skipTest('Native platform factory not available')
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

        if not native_platform_factory_available:
            self.skipTest('Native platform factory not available')

        factory = get_platform_factory()
        self.assertIsNotNone(factory)
        self.assertNotEquals(factory, toga_dummy.factory)
