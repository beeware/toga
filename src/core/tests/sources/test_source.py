from unittest import TestCase
from unittest.mock import Mock

from toga.sources import Source


class SourceTests(TestCase):
    def test_listeners(self):
        listener1 = Mock()
        source = Source()

        source.add_listener(listener1)
        self.assertListEqual(source.listeners, [listener1])

        # activate listener
        source._notify('message1')
        listener1.message1.assert_called_once_with()

        # activate listener with data
        source._notify('message2', arg1=11, arg2=22)
        listener1.message2.assert_called_once_with(arg1=11, arg2=22)

        # add more widgets to listeners
        listener2 = Mock()
        source.add_listener(listener2)
        self.assertListEqual(source.listeners, [listener1, listener2])

        # activate listener
        source._notify('message3')
        listener1.message3.assert_called_once_with()
        listener2.message3.assert_called_once_with()

        # activate listener with data
        source._notify('message4', arg1=11, arg2=22)
        listener1.message4.assert_called_once_with(arg1=11, arg2=22)
        listener2.message4.assert_called_once_with(arg1=11, arg2=22)

        # remove from listeners
        source.remove_listener(listener2)
        self.assertListEqual(source.listeners, [listener1])

    def test_missing_listener_method(self):
        listener1 = object()
        source = Source()

        source.add_listener(listener1)

        # This shouldn't raise an error
        source._notify('message1')
