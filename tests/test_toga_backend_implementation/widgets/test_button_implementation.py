import unittest


# BUTTON DEFINITIONS
# if the button core API changes it should be reflected here with a new
# 'check_requirements_of_version_<new_version>' function.
def check_requirements_of_version_0_1_0(self):
    # Here we check if the button-implementation-requirements of version 0.1.0 are fulfilled.
    # TODO implement a more robust way of checking if the requirements are meet. ast or re module maybe?
    self.assertIn('class Button(', self.FILE)
    self.assertIn('self._create()', self.FILE)
    self.assertIn('def create(self):', self.FILE)
    self.assertIn('def _set_label(self,', self.FILE)


# TEST PLATFORM IMPLEMENTATIONS OF TOGA BUTTON
class TestAndroidButtonImplementation(unittest.TestCase):
    __version__ = '0.1.0'

    @classmethod
    def setUpClass(cls):
        with open('./src/android/toga_android/widgets/button.py', 'r') as f:
            cls.FILE = f.read()

    @unittest.skipIf(__version__ < '0.1.0', 'Implementation of Button does not comply with button version 0.1.0')
    def test_button_requirements_of_version_0_1_0(self):
        check_requirements_of_version_0_1_0(self)

#
class TestCocoaButtonImplementation(unittest.TestCase):
    __version__ = '0.1.0'

    @classmethod
    def setUpClass(cls):
        with open('./src/cocoa/toga_cocoa/widgets/button.py', 'r') as f:
            cls.FILE = f.read()

    @unittest.skipIf(__version__ < '0.1.0', 'Implementation of Button does not comply with button version 0.1.0')
    def test_button_requirements_of_version_0_1_0(self):
        check_requirements_of_version_0_1_0(self)


class TestDjangoButtonImplementation(unittest.TestCase):
    __version__ = '0.1.0'

    @classmethod
    def setUpClass(cls):
        with open('./src/django/toga_django/widgets/button.py', 'r') as f:
            cls.FILE = f.read()

    @unittest.skipIf(__version__ < '0.1.0', 'Implementation of Button does not comply with button version 0.1.0')
    def test_button_requirements_of_version_0_1_0(self):
        check_requirements_of_version_0_1_0(self)


class TestGTKButtonImplementation(unittest.TestCase):
    __version__ = '0.1.0'

    @classmethod
    def setUpClass(cls):
        with open('./src/gtk/toga_gtk/widgets/button.py', 'r') as f:
            cls.FILE = f.read()

    @unittest.skipIf(__version__ < '0.1.0', 'Implementation of Button does not comply with button version 0.1.0')
    def test_button_requirements_of_version_0_1_0(self):
        check_requirements_of_version_0_1_0(self)


class TestIOSButtonImplementation(unittest.TestCase):
    __version__ = '0.1.0'

    @classmethod
    def setUpClass(cls):
        with open('./src/iOS/toga_iOS/widgets/button.py', 'r') as f:
            cls.FILE = f.read()

    @unittest.skipIf(__version__ < '0.1.0', 'Implementation of Button does not comply with button version 0.1.0')
    def test_button_requirements_of_version_0_1_0(self):
        check_requirements_of_version_0_1_0(self)


class TestWin32ButtonImplementation(unittest.TestCase):
    __version__ = '0.0.0'

    @classmethod
    def setUpClass(cls):
        with open('./src/win32/toga_win32/widgets/button.py', 'r') as f:
            cls.FILE = f.read()

    @unittest.skipIf(__version__ < '0.1.0', 'Implementation of Button does not comply with button version 0.1.0')
    def test_button_requirements_of_version_0_1_0(self):
        check_requirements_of_version_0_1_0(self)


class TestWinformsButtonImplementation(unittest.TestCase):
    __version__ = '0.1.0'

    @classmethod
    def setUpClass(cls):
        with open('./src/winforms/toga_winforms/widgets/button.py', 'r') as f:
            cls.FILE = f.read()

    @unittest.skipIf(__version__ < '0.1.0', 'Implementation of Button does not comply with button version 0.1.0')
    def test_button_requirements_of_version_0_1_0(self):
        check_requirements_of_version_0_1_0(self)
