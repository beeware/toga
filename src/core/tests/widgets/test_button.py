import toga
import toga_dummy
from toga_dummy.utils import TestCase


class ButtonTests(TestCase):
    def setUp(self):
        super().setUp()

        # Create a button with the dummy factory
        self.initial_text = 'Test Button'
        self.btn = toga.Button(self.initial_text, factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.btn._impl.interface, self.btn)
        self.assertActionPerformed(self.btn, 'create Button')

    def test_button_text(self):
        self.assertEqual(self.btn._text, self.initial_text)
        self.btn.text = 'New Text'
        self.assertEqual(self.btn.text, 'New Text')

        # test if backend gets called with the right text
        self.assertValueSet(self.btn, 'text', 'New Text')

    def test_button_text_with_None(self):
        self.btn.text = None
        self.assertEqual(self.btn.text, '')
        self.assertValueSet(self.btn, 'text', '')

    def test_button_on_press(self):
        self.assertIsNone(self.btn._on_press)

        # set a new callback
        def callback(widget, **extra):
            return 'called {} with {}'.format(type(widget), extra)

        self.btn.on_press = callback
        self.assertEqual(self.btn.on_press._raw, callback)
        self.assertEqual(
            self.btn.on_press('widget', a=1),
            "called <class 'toga.widgets.button.Button'> with {'a': 1}"
        )
        self.assertValueSet(self.btn, 'on_press', self.btn.on_press)

    def test_focus(self):
        self.btn.focus()
        self.assertActionPerformed(self.btn, "focus")

    ######################################################################
    # 2022-07: Backwards compatibility
    ######################################################################

    def test_label_deprecated(self):
        new_text = 'New Label'
        with self.assertWarns(DeprecationWarning):
            self.btn.label = new_text
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(self.btn.label, new_text)
        self.assertValueSet(self.btn, 'text', new_text)

    def test_init_with_deprecated(self):
        # label is a deprecated argument
        with self.assertWarns(DeprecationWarning):
            toga.Button(
                label='Test Button',
                factory=toga_dummy.factory
            )

        # can't specify both label *and* text
        with self.assertRaises(ValueError):
            toga.Button(
                label='Test Button',
                text='Test Button',
                factory=toga_dummy.factory
            )

        # label/text is mandatory
        with self.assertRaises(TypeError):
            toga.Button(
                factory=toga_dummy.factory
            )

    ######################################################################
    # End backwards compatibility.
    ######################################################################
