import sys
import unittest
from unittest.mock import create_autospec, call, patch, PropertyMock, Mock
from toga.events import EventSourceMeta, EventSource, Event, UndefinedEventRaised


class EventSourceTests(unittest.TestCase):
    class ABaseWidget(EventSource):
        on_simple_event1 = Event('Simple Event 1')
        on_simple_event2 = Event('Simple Event 2')

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self._impl = Mock(spec_set=['set_event_handler'])

    def setUp(self):
        super().setUp()

        @create_autospec
        def callback1(widget):
            pass

        @create_autospec
        def callback2(widget, arg1, arg2):
            pass

        self.callback1 = callback1
        self.callback2 = callback2

    def test_event_attrs(self):
        bw = self.ABaseWidget(factory=self)
        self.assertIsNone(bw.on_simple_event1)
        self.assertIsNone(bw.on_simple_event2)

        bw.on_simple_event1 = self.callback1
        self.assertEqual(bw.on_simple_event1, self.callback1)
        self.assertIsNone(bw.on_simple_event2)

        bw.on_simple_event2 = self.callback2
        self.assertEqual(bw.on_simple_event1, self.callback1)
        self.assertEqual(bw.on_simple_event2, self.callback2)

        self.assertListEqual(bw._impl.set_event_handler.mock_calls, [
            call('on_simple_event1', self.callback1),
            call('on_simple_event2', self.callback2),
        ])

    def test_event_init_args(self):
        bw = self.ABaseWidget(
            factory=self,
            on_simple_event1=self.callback2,
            on_simple_event2=self.callback1,
        )
        self.assertEqual(bw.on_simple_event1, self.callback2)
        self.assertEqual(bw.on_simple_event2, self.callback1)

        self.assertListEqual(sorted(bw._impl.set_event_handler.mock_calls), [
            call('on_simple_event1', self.callback2),
            call('on_simple_event2', self.callback1),
        ])

    @patch('toga.events.wrapped_handler')
    def test_callback_call(self, wrapped_handler):
        bw = self.ABaseWidget(
            factory=self,
            on_simple_event1=self.callback1
        )
        self.assertEqual(bw.on_simple_event1, self.callback1)
        self.assertIsNone(bw.on_simple_event2)

        bw.raise_event('on_simple_event1')
        self.assertListEqual(wrapped_handler.mock_calls, [
            call(bw, self.callback1), call(bw, self.callback1)(bw)
        ])
        wrapped_handler.reset_mock()

        bw.raise_event('on_simple_event2')
        self.assertListEqual(wrapped_handler.mock_calls, [])

    @patch('toga.events.wrapped_handler')
    def test_callback_call_w_args(self, wrapped_handler):
        bw = self.ABaseWidget(
            factory=self,
            on_simple_event1=self.callback1
        )

        bw.raise_event('on_simple_event1', 'arg1', kwarg1='val1')
        self.assertListEqual(wrapped_handler.mock_calls, [
            call(bw, self.callback1),
            call(bw, self.callback1)(bw, 'arg1', kwarg1='val1')
        ])

    @patch('toga.events.wrapped_handler')
    def test_raise_missing_event(self, wrapped_handler):
        bw = self.ABaseWidget(
            factory=self,
            on_simple_event1=self.callback1
        )

        with self.assertRaises(UndefinedEventRaised):
            bw.raise_event('on_simple_event3')

    @patch('toga.events.wrapped_handler')
    def test_event_inheritance(self, wrapped_handler):

        class ASubWidget(self.ABaseWidget):
            on_simple_event3 = Event('Event on subclass')

        sw = ASubWidget(
            factory=self,
            on_simple_event1=self.callback1,
            on_simple_event3=self.callback2,
        )
        print(type(sw).__dict__)
        self.assertEqual(sw.on_simple_event1, self.callback1)
        self.assertIsNone(sw.on_simple_event2)
        self.assertEqual(sw.on_simple_event3, self.callback2)

        sw.raise_event('on_simple_event1')
        sw.raise_event('on_simple_event2')
        sw.raise_event('on_simple_event3')
        self.assertListEqual(wrapped_handler.mock_calls, [
            call(sw, self.callback1), call(sw, self.callback1)(sw),
            call(sw, self.callback2), call(sw, self.callback2)(sw),
        ])
        with self.assertRaises(UndefinedEventRaised):
            sw.raise_event('on_simple_event4')

    def test_event_method_call_on_raise(self):
        """We check here that raising events is done via calling a method on
        the Event descriptor object. This ensures that derived descriptor
        classes can implement new callback calling patterns
        """
        EventMock = PropertyMock(
            spec_set=['raise_event', '__class__'], __class__=Event
        )

        class AWidget(EventSource):
            on_event = EventMock

        widg = AWidget(on_event=self.callback1)
        widg.raise_event('on_event')
        widg.raise_event('on_event', 'arg1', 'arg2')

        self.assertListEqual(EventMock.mock_calls, [
            call(self.callback1),
            call.raise_event(widg),
            call.raise_event(widg, 'arg1', 'arg2'),
        ])


class EventSourceMetaTests(unittest.TestCase):
    def test_metaclass(self):
        self.assertIsInstance(EventSource, EventSourceMeta)
        # Make sure that EventSourceMeta is simply an alias to `type` in Python>3.5
        if sys.version_info.major == 3 and sys.version_info.minor <= 5:
            self.assertTrue(issubclass(EventSourceMeta, type))
            self.assertNotEqual(EventSourceMeta, type)
        else:
            self.assertEqual(EventSourceMeta, type)
