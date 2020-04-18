import toga
import toga_dummy
from toga_dummy.utils import TestCase, TestStyle


class ScrollContainerTests(TestCase):
    def setUp(self):
        super().setUp()

        self.sc = toga.ScrollContainer(style=TestStyle(), factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.sc._impl.interface, self.sc)
        self.assertActionPerformed(self.sc, 'create ScrollContainer')

    def test_set_content_with_widget(self):
        self.assertEqual(self.sc.content, None, 'The default value of content should be None')

        new_content = toga.Box(style=TestStyle(), factory=toga_dummy.factory)
        self.sc.content = new_content
        self.assertEqual(self.sc.content, new_content)
        self.assertEqual(self.sc._content, new_content)
        self.assertActionPerformedWith(self.sc, 'set content', widget=new_content._impl)

        self.assertActionPerformedWith(new_content, 'set bounds', x=0, y=0, width=0, height=0)

    def test_set_content_with_None(self):
        new_content = None
        self.assertEqual(self.sc.content, new_content)
        self.assertEqual(self.sc._content, new_content)
        self.assertActionNotPerformed(self.sc, 'set content')

    def test_vertical_property(self):
        self.assertEqual(self.sc.vertical, True, 'The default should be True')

        new_value = False
        self.sc.vertical = new_value
        self.assertEqual(self.sc.vertical, new_value)
        self.assertValueSet(self.sc, 'vertical', new_value)

    def test_horizontal_property(self):
        self.assertEqual(self.sc.horizontal, True, 'The default should be True')

        new_value = False
        self.sc.horizontal = new_value
        self.assertEqual(self.sc.horizontal, new_value)
        self.assertValueSet(self.sc, 'horizontal', new_value)

    def test__set_window_without_content(self):
            # sc and window default value is None
            self.assertIsNotNone(self.sc)
            self.assertIsNone(self.sc.window)
            
            self.sc.window = toga.window
            self.assertEqual(self.sc.window, toga.window)
            
            # children remains None when window is set
            self.assertIsNone(self.sc._children)
            self.assertValueSet(self.sc, 'window', toga.window)

            # test that error is raised when setting a window to empty ScrollContainer
            self.sc = None
            with self.assertRaises(AttributeError):
                self.sc.window = toga.window

    def test__set_window_with_Content(self):
            # window default value is None
            self.assertIsNone(self.sc.window)
            
            new_content = toga.Box(style=TestStyle(), factory=toga_dummy.factory)
            self.sc.content = new_content
            self.assertActionPerformed(self.sc, 'set content')

            self.sc.window = toga.window
            self.assertEqual(self.sc.window, toga.window)
            self.assertValueSet(self.sc, 'window', toga.window)
