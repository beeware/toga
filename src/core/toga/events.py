"""toga.events - Base classes for objects that expose events

This module defines classes to be used for creating objects that need to expose
events in a way that allows other objects to set callback to be called when
event occur. An example for this is Widgets that invoke callbacks when users
interact with them.

Here is an example of how to use the classes that can be found here.

    >>> class AClickableWidget(EventSource):
    ...     on_click = Event('Called when widget is clicked')
    ...
    ...     def __init__(self, *args, **kwargs):
    ...         super().__init__(*args, **kwargs)
    ...         # This is typically done via the `factory` argument
    ...         self._impl = AClickableWidgetBackend(interface=self)
    ...
    >>> class AClickableWidgetBackend:
    ...     def __init__(self, interface):
    ...         self.interface = interface
    ...
    ...     def emulate_click(self, which_button):
    ...         self.interface.raise_event('on_click', which_button)
    ...
    >>> def click_handler(widget, which_button):
    ...     print(f"I was clicked with {which_button} mouse button!")
    ...
    >>> widget = AClickableWidget(on_click=click_handler)
    >>> widget._impl.emulate_click("Left")
    I was clicked with Left mouse button!
    >>> widget._impl.emulate_click("Right")
    I was clicked with Right mouse button!

Note: Typically only top-level classes such as `Widget` or `Window` should
inherit directly from `EventSource`, others should inherit from those classes
instead.
"""
import sys

from toga.handlers import wrapped_handler


if sys.version_info.major == 3 and sys.version_info.minor <= 5:
    # Polyfill the calling to __set_name__ for Python<=3.5

    class EventSourceMeta(type):
        def __new__(mcs, name, bases, attrs, **kwargs):
            cls = super().__new__(mcs, name, bases, attrs, **kwargs)
            # Call __set_name__ like Python>3.5 does (almost)
            for aname, avalue in attrs.items():
                set_name = getattr(avalue, '__set_name__', None)
                if set_name is None:
                    continue
                set_name(cls, aname)
            return cls

else:
    EventSourceMeta = type


class EventSource(metaclass=EventSourceMeta):
    """Base class for classes that can have event callbacks

    All keyword arguments passed to this class become attempts at setting event
    callbacks.

    Objects of this class are not meant to be used directly. Instead, other
    classes that wish to be able to call event callbacks should inherit from it
    and then define some events using the Event descriptor class.
    """
    def __init__(self, *args, **kwargs):
        event_attrs = []
        non_event_kwargs = {}
        for arg, callback in kwargs.items():
            attr = self._get_event_descriptor(arg)
            if attr is None or not isinstance(attr, Event):
                non_event_kwargs[arg] = callback
                continue
            event_attrs.append((attr, callback))
        super().__init__(*args, **non_event_kwargs)
        for attr, callback in event_attrs:
            attr.__set__(self, callback)

    def raise_event(self, event, *args, **kwargs):
        """Call the callback associated with an event, if any

        Args:
            event (str): The name of the event to raise callbacks for

        All other positional and keyword arguments are passed to the callback
        function. If a bad event string is passed, UndefinedEventRaised
        exception is raised.
        """
        descr = self._get_event_descriptor(event)
        if descr is None:
            raise UndefinedEventRaised(event)
        descr.raise_event(self, *args, **kwargs)

    @classmethod
    def _get_event_descriptor(cls, event):
        # Its unfortunate, but it seems there is no method or function that is
        # internal to the interpreter and that we could use to scan the MRO
        # and access the descriptor object without also masking it away and
        # implicitly calling its __get__ or __set__ methods.
        for klass in cls.mro():
            descriptor = klass.__dict__.get(event)
            if descriptor is None:
                continue
            if isinstance(descriptor, Event):
                return descriptor
            else:
                return None
        else:
            return None


class Event:
    """Descriptor class for event callback attributes

    Args:
        doc (str): Documentation string for the event
    """
    def __init__(self, doc=None):
        self.__doc__ = doc

    def __repr__(self):
        return '{} Event'.format(self._name or "Unnamed")

    def __set_name__(self, owner, name):
        self._name = name
        self._attr_name = '_{}'.format(name)

    def __get__(self, instance, owner):
        if instance is None:
            return None
        return getattr(instance, self._attr_name, None)

    def __set__(self, instance, callback):
        setattr(instance, self._attr_name, callback)

    def raise_event(self, instance, *args, **kwargs):
        """Call the callback associated with the event, if any

        Args:
            instance (:obj:`EventSource`): A widget to call the event for

        All other arguments are passed on the the callback
        """
        callback = self.__get__(instance, type(instance))
        if callback is None:
            return
        wrapped_handler(instance, callback)(instance, *args, **kwargs)


class UndefinedEventRaised(AttributeError):
    """Exception class to be raised when an attempt is made to invoke the
    callbacks for a nonexistent event attribute
    """
