from unittest.mock import Mock
from weakref import ref

from toga.sources import Listener, Source


def test_notify():
    source = Source()

    # No listeners
    assert source.listeners == []
    source.notify("message0")

    listener1 = Mock()

    source.add_listener(listener1)
    assert source.listeners == [listener1]

    # Add the same listener a second time
    source.add_listener(listener1)
    assert source.listeners == [listener1]

    # activate listener
    source.notify("message1")
    listener1.message1.assert_called_once_with()

    # activate listener with data
    source.notify("message2", arg1=11, arg2=22)
    listener1.message2.assert_called_once_with(arg1=11, arg2=22)

    # add more widgets to listeners
    listener2 = Mock()
    source.add_listener(listener2)
    assert source.listeners == [listener1, listener2]

    # activate listener
    source.notify("message3")
    listener1.message3.assert_called_once_with()
    listener2.message3.assert_called_once_with()

    # activate listener with data
    source.notify("message4", arg1=11, arg2=22)
    listener1.message4.assert_called_once_with(arg1=11, arg2=22)
    listener2.message4.assert_called_once_with(arg1=11, arg2=22)

    # remove listener2
    source.remove_listener(listener2)
    assert source.listeners == [listener1]

    # Activate listeners; listener2 not notified.
    source.notify("message5")
    listener1.message5.assert_called_once_with()
    listener2.message5.assert_not_called()

    # remove listener2 again should not error
    source.remove_listener(listener2)
    assert source.listeners == [listener1]


def test_missing_listener_method():
    """If a listener doesn't implement a notification method, the notification is
    ignored."""
    full_listener = Mock()

    class PartialListener:
        pass

    partial_listener = PartialListener()
    source = Source()

    source.add_listener(full_listener)
    source.add_listener(partial_listener)
    assert source.listeners == [full_listener, partial_listener]

    # This shouldn't raise an error
    source.notify("message1")

    full_listener.message1.assert_called_once_with()


def test_deleted_listener():
    """If a listener is deleted it should be removed from the source."""

    class MyListener(Listener):
        pass

    listener = MyListener()
    listener_ref = ref(listener)
    source = Source()

    source.add_listener(listener)
    assert source.listeners == [listener]

    # drop our reference to listener
    del listener

    assert source.listeners == []

    # if we try to remove the weakref later, no errors
    # this shouldn't happen in normal usage, but might if
    # something grabs references to the weakrefs inside the
    # source
    source._remove_deleted(listener_ref)
