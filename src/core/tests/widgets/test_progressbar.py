import toga
import toga_dummy
from toga_dummy.utils import TestCase

"""
### ProgressBar truth table

Assuming ProgressBar has three attributes: `max`, `running`, and `value`

| max     | running   | value     | Behavior                |
|---------|-----------|-----------|-------------------------|
| None    | False     | None      | disabled                |
| None    | False     | number    | disabled                |
| None    | True      | None      | indeterminate anim.     |
| None    | True      | number    | indeterminate anim.     |
| number  | False     | None      | show 0%                 |
| number  | False     | number    | show percentage         |
| number  | True      | None      | show 0%, working anim.  |
| number  | True      | number    | show %, working anim.   |

The table can be reduced since the value is rendered the same
regardless of it being None or not

| max     | running   | Behavior                |
|---------|-----------|-------------------------|
| None    | False     | disabled                |
| None    | True      | indeterminate anim.     |
| number  | False     | show percentage         |
| number  | True      | show %, working anim.   |

Ultimately, the question is about what should be done when the progress bar has
a `max` but its `value` happens to be None. Personally, I feel that it should
render as if the value were zero.
"""

class ProgressBarTests(TestCase):
    def setUp(self):
        super().setUp()

        self.progress_bar = toga.ProgressBar(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.progress_bar._impl.interface, self.progress_bar)
        self.assertActionPerformed(self.progress_bar, 'create ProgressBar')

    def test_set_max_to_number(self):
        new_max = 100
        self.progress_bar.max = new_max
        self.assertEqual(self.progress_bar._max, new_max)
        self.assertValueSet(self.progress_bar, 'max', value=new_max)

    def test_set_max_to_none(self):
        self.progress_bar.max = None
        self.assertEqual(self.progress_bar._max, None)
        self.assertValueSet(self.progress_bar, 'max', value=None)

    def test_set_running(self):
        self.progress_bar.running = False
        self.assertEqual(self.progress_bar._running, False)

        self.progress_bar.running = True
        self.assertEqual(self.progress_bar._running, True)
        self.assertValueSet(self.progress_bar, 'running', value=True)

        self.progress_bar.running = False
        self.assertValueSet(self.progress_bar, 'running', value=False)

    def test_set_value_to_number_less_than_max(self):
        new_value = self.progress_bar.max / 2;
        self.progress_bar.value = new_value
        self.assertEqual(self.progress_bar._value, new_value)
        self.assertValueSet(self.progress_bar, 'value', value=new_value)

    def test_set_value_to_number_greater_than_max(self):
        new_value = self.progress_bar.max + 1;
        self.progress_bar.value = new_value
        self.assertEqual(self.progress_bar._value, self.progress_bar.max)
        self.assertValueSet(self.progress_bar, 'value', value=new_value)

    def test_set_value_to_none(self):
        self.progress_bar.value = None
        self.assertEqual(self.progress_bar._value, 0) # 0 is clean value for None
        self.assertValueSet(self.progress_bar, 'value', value=None)

    def test_disabled_cases(self):
        # Start with a default progress bar
        self.progress_bar = toga.ProgressBar(factory=toga_dummy.factory)
        self.assertTrue(self.progress_bar.enabled)

        # It should be disabled if both max and running are falsy

        self.progress_bar.max = None
        self.progress_bar.running = False
        self.progress_bar.value = 0
        self.assertFalse(self.progress_bar.enabled)

        #self.progress_bar.max = None
        self.progress_bar.running = True
        #self.progress_bar.value = 0
        self.assertTrue(self.progress_bar.enabled)

        self.progress_bar.max = 1
        self.progress_bar.running = False
        #self.progress_bar.value = 0
        self.assertTrue(self.progress_bar.enabled)
