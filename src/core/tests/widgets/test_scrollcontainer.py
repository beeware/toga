from unittest import mock
import toga
import toga_dummy
from toga_dummy.utils import TestCase, TestStyle


class ScrollContainerTests(TestCase):
    def setUp(self):
        super().setUp()

        self.on_scroll = mock.Mock()
        self.sc = toga.ScrollContainer(
            style=TestStyle(), factory=toga_dummy.factory, on_scroll=self.on_scroll
        )

    def test_widget_created(self):
        self.assertEqual(self.sc._impl.interface, self.sc)
        self.assertActionPerformed(self.sc, 'create ScrollContainer')

    def test_on_scroll_is_set(self):
        self.assertValueSet(self.sc, "on_scroll", self.on_scroll)
        self.assertEqual(self.sc.on_scroll, self.on_scroll)

    def test_initial_scroll_position_is_zero(self):
        self.assertEqual(self.sc.horizontal_position, 0)
        self.assertEqual(self.sc.vertical_position, 0)

    def test_set_horizontal_scroll_position(self):
        horizontal_position = 0.5
        self.sc.horizontal_position = horizontal_position
        self.assertValueSet(self.sc, "horizontal_position", horizontal_position)
        self.assertEqual(self.sc.horizontal_position, horizontal_position)
        self.assertEqual(self.sc.vertical_position, 0)

    def test_set_vertical_scroll_position(self):
        vertical_position = 0.5
        self.sc.vertical_position = vertical_position
        self.assertValueSet(self.sc, "vertical_position", vertical_position)
        self.assertEqual(self.sc.horizontal_position, 0)
        self.assertEqual(self.sc.vertical_position, vertical_position)

    def test_set_content_with_widget(self):
        self.assertEqual(
            self.sc.content, None, 'The default value of content should be None'
        )

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

    def test_set_horizontal_position_when_unset_raises_an_error(self):
        self.sc.horizontal = False
        with self.assertRaisesRegex(
            ValueError, "^Cannot set horizontal position when horizontal is not set.$"
        ):
            self.sc.horizontal_position = 0.5

    def test_set_vertical_position_when_unset_raises_an_error(self):
        self.sc.vertical = False
        with self.assertRaisesRegex(
            ValueError, "^Cannot set vertical position when vertical is not set.$"
        ):
            self.sc.vertical_position = 0.5

    def test_set_app(self):

        new_content = toga.Box(style=TestStyle(), factory=toga_dummy.factory)
        self.sc.content = new_content
        self.assertIsNone(new_content.app)

        app = mock.Mock()
        self.sc.app = app
        self.assertEqual(new_content.app, app)
