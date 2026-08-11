from typing import ClassVar

from win32more import ComError

from toga import App
from toga.handlers import WeakrefCallable

"""A handler to be used with WinUI 3 native events.

The need for this module arises from the requirements of `build_cleanup_test` from the
testbed. In particular, the callback needs to be assigned with a weak reference since
the native process will hold onto it reference after cleanup.

Assigning the callback with a weak reference leads to another issue: The underlying
native process may still have a callback scheduled after the python callback function
has been garbage collect. This lead to the second purpose of this module, which is to
cleanup and avoid any dangling pointers.
"""


class NativeEvent:
    _cleared_callbacks: ClassVar[dict] = {}

    def __init__(self, owner, name: str):
        """Manages the adding and clearing of callbacks of a native instance event.

        :param owner: The native instance that is triggering the event callback e.g. an
        instance of `Microsoft.UI.Xaml.Window`.
        :param name: The name of the event as a property of the owner e.g. Activated.
            Note that recursive properties of sub-properties can be accessed by
            replacing `.` with `_`. For example, `instance.AppWindow.Changed` is
            accessed using the the name `AppWindow_Changed`.
        """
        split_name = name.split("_")

        self._owner = owner
        for attribute in split_name[:-1]:
            self._owner = getattr(self._owner, attribute)

        self._name = split_name[-1]
        self._registry = {}

    def __iadd__(self, callback):
        """Add a callback for the event."""
        event_adder = getattr(self._owner, "add_" + self._name)

        # Don't allow the external process to keep a reference to the callback.
        token = event_adder(WeakrefCallable(callback))

        # Keep a local reference to the callback.
        self._registry[id(token)] = (token, callback)

        return self

    def clear(self):
        """Clear all callbacks for the event."""
        event_remover = getattr(self._owner, "remove_" + self._name)
        for token, callback in self._registry.values():
            try:
                event_remover(token)

            except ComError:
                # This error occurs when the actual WinUI 3 object has been removed, for
                # example when its parent is destroyed, but the python win32more object
                # remains. Since the actual WinUI 3 object has been removed, and hence
                # will not raise any events, this error is ignored.
                pass

            NativeEvent._clear_callback(callback)

        self._registry = {}

    @classmethod
    def _clear_callback(cls, callback):
        loop = App.app.loop
        # There is potentially still a call to the callback in the message queue
        # after the event has been deregistered. So the task to clear the callback
        # is placed at the back of the queue, and only deletes the
        # reference to the callback after any calls have been made.
        if not loop.is_closed():
            callback_id = id(callback)
            cls._cleared_callbacks[callback_id] = callback

            def clear_callback_task(cls=cls, callback_id=callback_id):
                del cls._cleared_callbacks[callback_id]

            App.app.loop.call_soon_threadsafe(clear_callback_task)
        # If the loop is closed then there is no need to wait for the event to be
        # deregistered. This branch is part of the shutdown procedure so it is marked
        # as no cover.
        else:  # pragma: no cover
            callback = None


class NativeEventsHandler:
    def __init__(self, owner):
        """A handler that interfaces with the NativeEvent objects of a native instance.

        :param owner: The native instance that is triggering the event callbacks e.g. an
            instance of `Microsoft.UI.Xaml.Window`.
        """
        self._owner = owner
        self._event_registry = {}

    def __getattr__(self, event_name):
        """Get (or creates, registers and gets) the NativeEvent object for an event."""
        if not event_name[0].isupper():  # pragma: no cover
            raise ValueError("Native events use the PascalCase naming convention.")

        if event_name not in self._event_registry:
            self._event_registry[event_name] = NativeEvent(self._owner, event_name)

        return self._event_registry[event_name]

    def __setattr__(self, name, value):
        if not name[0].isupper():
            super().__setattr__(name, value)
            return

        # If the name has a capital first letter, assume it is an event name.
        self._event_registry[name] = value

    def clear(self):
        """Clears all the registered NativeEvent objects."""
        for event in self._event_registry.values():
            event.clear()

        self._event_registry = {}


class NativeEventsMixin:
    """Methods used to manage and clean-up the events for a native instance."""

    @property
    def native_class(self):
        return type(self).__bases__[1]

    def __del__(self):
        if getattr(self, "_event_handler", None):
            self.event_handler.clear()

        # This is a safety catch for future changes in the native backend.
        if hasattr(self.native_class, "__del__"):  # pragma: no cover
            super().__del__()

    @property
    def event_handler(self):
        # Lazy load an EventHandler instance.
        if not getattr(self, "_event_handler", None):
            self._event_handler = NativeEventsHandler(self)

        return self._event_handler


def events_handled(native_cls):
    """Dynamically creates a native class with handled events."""
    cls_name = native_cls.__name__ + "Handled"
    bases = (NativeEventsMixin, native_cls)
    return type(cls_name, bases, {})()


class EventsHandledMixin:
    """Methods to allow the easy instantiation of a native class with handled events."""

    @property
    def native_cls(self):
        return self._native_cls if hasattr(self, "_native_cls") else None

    @native_cls.setter
    def native_cls(self, cls):
        self._native_cls = cls
        self.native = events_handled(cls)
