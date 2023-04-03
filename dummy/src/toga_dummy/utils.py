import sys
import unittest
from unittest.mock import Mock

import pytest
from travertino.declaration import BaseStyle
from travertino.layout import BaseBox
from travertino.size import BaseIntrinsicSize


def not_required(method_or_class):
    """This decorator function is used to mark methods or classes that they are
    not required for interface compliance.

    :param method_or_class: The method or class to decorate
    :returns: The method or class being decorated
    """
    return method_or_class


def not_required_on(*args):
    """This decorator function is used to mark methods or classes that they are
    not required on certain platforms. This is only used by the implementation
    checks creation mechanism.

    Examples:
        >>> # Marks the function as only required on platforms that are not "mobile".
        >>> @not_required_on('mobile')
        >>> def open_window():
        >>>     self.window.open()

        >>> # Function is not required on "mobile" and "gtk" backends.
        >>> @not_required_on('mobile', 'gtk')
        >>> def open_window():
        >>>     self.window.open()

    :param args: The platform(s) on which the method or class isn't required.
        Can accept a specific backend (e.g., `gtk`, `iOS`), or a class of platform
        (e.g., `mobile`, `desktop`).
    :returns: The method or class being decorated
    """

    def _dec(method_or_class):
        return method_or_class

    return _dec


###########################################################################
# The event types that can be logged
###########################################################################


class EventLog:
    # Event types that can be logged
    SET_VALUE = "set attribute"
    GET_VALUE = "get attribute"
    ACTION = "action"

    _log = []
    _next_sequence = 0

    @classmethod
    def reset(cls):
        cls._log.clear()
        cls._next_sequence = 0

    @classmethod
    def next_sequence_value(cls):
        cls._next_sequence += 1
        return cls._next_sequence

    @classmethod
    def log(cls, logtype, instance, **context):
        """Add an entry to the event log.

        :param logtype: The type of object being logged (SET_VALUE, etc)
        :param instance: The instance that generated loggable activity
        :param context: A dictionary of data related to the event. The contents
            of the dictionary will depend on the event that occurred.
        :returns: The sequence value of the log entry
        """
        entry = LogEntry(logtype, instance, **context)
        cls._log.append(entry)
        return entry.sequence

    @classmethod
    def values(cls, instance, attr):
        """Return all values that an attribute on an instance has had.

        :param instance: The widget instance
        :param attr: The attribute name to inspect
        :return: A list of all values that have been assigned to the attribute.
            Raises AttributeError if the attribute has not been set on the instance.
        """
        attrs = set()
        values = []
        for entry in cls._log:
            if entry.logtype == cls.SET_VALUE and entry.instance == instance._impl:
                if entry.context["attr"] == attr:
                    values.append(entry.context["value"])
                else:
                    attrs.add(entry.context["attr"])

        if values:
            return values

        if attrs:
            known_attributes = ", ".join(f"{a!r}" for a in sorted(attrs))
            raise AttributeError(
                f"{instance} did not have the attribute {attr!r} set; "
                f"known attributes were {known_attributes}."
            )
        else:
            raise AttributeError(f"No attributes were set on {instance} ")

    @classmethod
    def value(cls, instance, attr):
        """Return the current value of an attribute on an instance.

        :param instance: The widget instance
        :param attr: The attribute name to inspect
        :return: The current value of the attribute on the instance. Raises
            AttributeError if the attribute has not been set on the instance.
        """
        attrs = set()
        for entry in cls._log[-1::-1]:
            if entry.logtype == cls.SET_VALUE and entry.instance == instance._impl:
                if entry.context["attr"] == attr:
                    return entry.context["value"]
                else:
                    attrs.add(entry.context["attr"])

        if attrs:
            known_attributes = ", ".join(f"{a!r}" for a in sorted(attrs))
            raise AttributeError(
                f"{instance} did not have the attribute {attr!r} set; "
                f"known attributes were {known_attributes}."
            )
        else:
            raise AttributeError(f"No attributes were set on {instance} ")

    @classmethod
    def retrieved(cls, instance, attr):
        """Determine if an attempt has been made to retrieve the value of an
        attribute.

        This only includes "normal" attribute access; retrievals made for test
        purposes are *not* included.

        :param instance: The widget instance
        :param attr: The attribute name to inspect
        :return: True if the attribute has been retrieved. Raises AttributeError
            if no attempt to retrieve the attribute has been made.
        """
        attrs = set()
        for entry in cls._log:
            if entry.logtype == cls.GET_VALUE and entry.instance == instance._impl:
                if entry.context["attr"] == attr:
                    return True
                else:
                    attrs.add(entry.context["attr"])

        if attrs:
            known_attributes = ", ".join(f"{a!r}" for a in sorted(attrs))
            raise AttributeError(
                f"{instance} did not retrieve the attribute {attr!r}; "
                f"known attribute retrievals are {known_attributes}."
            )
        else:
            raise AttributeError(f"No attributes were retrieved on {instance} ")

    @classmethod
    def performed_actions(cls, instance, action=None):
        """Return the details of all actions performed on an instance.

        :param instance: The widget instance
        :param action: (Optional) If provided, the list of actions will be
            filtered to *only* include the named action.
        :return: A list of individual actions that have been performed. Each
            entry is a dictionary consisting of the attributes used to invoke
            the action.
        """
        actions = set()
        details = []
        for entry in cls._log:
            if entry.logtype == cls.ACTION and entry.instance == instance._impl:
                if action is None or entry.context["action"] == action:
                    details.append(entry.context)
                else:
                    actions.add(entry.context["action"])

        if details:
            return details

        if actions:
            known_actions = ", ".join(f"{a!r}" for a in sorted(actions))
            raise AttributeError(
                f"{instance} did not perform the action {action!r}; "
                f"known actions were {known_actions}."
            )
        else:
            raise AttributeError(f"No actions were performed on {instance}")


class LogEntry:
    """An entry in the event log.

    :param logtype: The type of object being logged (SET_VALUE, etc)
    :param instance: The instance that generated loggable activity
    :param context: A dictionary of data related to the event. The contents of
        the dictionary will depend on the event that occurred.
    """

    def __init__(self, logtype, instance, **context):
        self.sequence = EventLog.next_sequence_value()
        self.logtype = logtype
        self.instance = instance
        self.context = context

    def __repr__(self):
        return f"<LogEntry: {self.logtype} on {self.instance}"


# A constant that can be used to differentiate between a value not being
# provided, and a value assuming a default value of None.
NOT_PROVIDED = object()


class LoggedObject:
    """A base class for objects on the dummy backend whose activity will be
    logged.

    Objects specified in the dummy backend should extend this class, and
    log any activity they perform using the methods on this object.
    """

    def _set_value(self, attr, value):
        """Set a value on the dummy object.

        Logs the new value for the attribute, and tracks it in the event log

        :param attr: The name of the attribute to set
        :param value: The new value for the attribute
        """
        EventLog.log(EventLog.SET_VALUE, instance=self, attr=attr, value=value)

    def _get_value(self, attr, default=NOT_PROVIDED):
        """Get a value on the dummy object.

        Logs the request for the attribute, and returns the most recent value
        set for the attribute.

        :param attr: The name of the attribute to get
        :param default: The default value for the attribute if it hasn't already
            been set.
        :returns: The value of the attribute, or ``default`` if the value has
            not been set.
        """
        EventLog.log(EventLog.GET_VALUE, instance=self, attr=attr)
        try:
            return EventLog.value(instance=self.interface, attr=attr)
        except AttributeError:
            if default is NOT_PROVIDED:
                raise
            return default

    def _action(self, action, **data):
        """Record that an action was performed on the object.

        :param action: The action that was performed
        :param data: Any data associated with the action.
        """
        EventLog.log(EventLog.ACTION, instance=self, action=action, **data)


class TestStyle(BaseStyle):
    __test__ = False

    class IntrinsicSize(BaseIntrinsicSize):
        pass

    class Box(BaseBox):
        pass

    def layout(self, root, viewport):
        pass


###########################################################################
# Pytest widget assertion helpers
###############################################################################


def attribute_value(_widget, _attr):
    """Retrieve the current value of a widget property.

    :param _widget: The interface of the widget to check
    :param _attr: The attribute to retrieve.
    :returns: The current value of the attribute
    """
    try:
        return EventLog.value(_widget, _attr)
    except AttributeError as e:
        pytest.fail(str(e))


def attribute_values(_widget, _attr):
    """Retrieve the list of values that the property has been set to.

    :param _widget: The interface of the widget to check
    :param _attr: The attribute to retrieve.
    :returns: The list of values to which the attribute has been set.
    """
    try:
        return EventLog.values(_widget, _attr)
    except AttributeError as e:
        pytest.fail(str(e))


def assert_attribute_retrieved(_widget, _attr):
    """Assert that the widget implementation attempted to retrieve an attribute.

    :param _widget: The interface of the widget to check
    :param _attr: The attribute to check.
    :returns: True if the attribute was retrieved
    """
    try:
        EventLog.retrieved(_widget, _attr)
    except AttributeError as e:
        pytest.fail(str(e))


def assert_attribute_not_retrieved(_widget, _attr):
    """Assert that the widget implementation did not attempt to retrieve an attribute.

    :param _widget: The interface of the widget to check
    :param _attr: The attribute to check.
    :returns: True if the attribute was *not* retrieved
    """
    try:
        EventLog.retrieved(_widget, _attr)
        pytest.fail(f"Widget {_widget} unexpectedly retrieved the attribute {_attr!r}.")
    except AttributeError:
        pass


def assert_attribute_not_set(_widget, _attr):
    """Assert that the widget implementation did not attempt to set an attribute.

    :param _widget: The interface of the widget to check
    :param _attr: The attribute to check.
    :returns: True if the attribute was not set
    """
    try:
        EventLog.values(_widget, _attr)
        pytest.fail(f"Widget {_widget} unexpectedly set the attribute {_attr!r}.")
    except AttributeError:
        pass


def assert_action_not_performed(_widget, _action):
    """Assert that the named action was *not* performed by a widget.

    :param _widget: The interface of the widget to check
    :param _action: The action to check.
    :returns: True if the action was not performed
    """
    try:
        EventLog.performed_actions(_widget, _action)
        pytest.fail(f"Action {_action!r} unexpectedly performed by {_widget}.")
    except AttributeError:
        pass


def assert_action_performed(_widget, _action):
    """Assert that the named action was performed by a widget.

    :param _widget: The interface of the widget to check
    :param _action: The action to check.
    :returns: True if the action was performed
    """
    try:
        EventLog.performed_actions(_widget, _action)
    except AttributeError as e:
        pytest.fail(str(e))


def assert_action_performed_with(_widget, _action, **test_data):
    """Assert if an action was performed with specific test data.

    :param _widget: The interface of the widget to check
    :param _action: The action to check.
    :param test_data: The arguments that should have been passed to the action.
    :returns: True if the action was performed
    """
    try:
        # Iterate over every action that was performed on
        # this object.
        for data in EventLog.performed_actions(_widget, _action):
            found = True
            # Iterate over every key and value in the test
            # data. If the value in the recorded action
            # doesn't match the requested value, then this isn't
            # a match.
            for key, value in test_data.items():
                try:
                    try:
                        # Look for a `_raw` attribute, as that will be the
                        # directly comparable object
                        raw = data[key]._raw
                        # If the _raw attribute is a mock, it doesn't actually exist
                        if isinstance(data[key]._raw, Mock):
                            raise AttributeError()

                        if raw != value:
                            found = False
                    except AttributeError:
                        # No raw attribute; use the provided value as-is
                        if data[key] != value:
                            found = False
                except KeyError:
                    found = False

            # Default behavior is to be found; so if we're
            # still in a "found" state, this action is a match
            # for the test data. Otherwise, reset, and try again
            # with the next recorded action.
            if found:
                return
    except AttributeError as e:
        # None of the recorded actions match the test data.
        pytest.fail(str(e))


###########################################################################
# Unittest widget assertions
#
# These have been (re)written in terms of Pytest assertions; this base
# class is deprecated and should not be used for new tests.
############################################################################
class TestCase(unittest.TestCase):
    def setUp(self):
        EventLog.reset()

        # We use the existence of a __main__ module as a proxy for being in test
        # conditions. This isn't *great*, but the __main__ module isn't meaningful
        # during tests, and removing it allows us to avoid having explicit "if
        # under test conditions" checks in paths.py.
        if "__main__" in sys.modules:
            del sys.modules["__main__"]

    def reset_event_log(self):
        EventLog.reset()

    def pytest_assert(self, assertion, *args, **kwargs):
        try:
            return assertion(*args, **kwargs)
        except AssertionError as e:
            self.fail(str(e))

    #####

    def assertValueSet(self, _widget, _attr, value):
        """Assert that the widget implementation has set an attribute to a
        value.

        Args:
            _widget: The interface of the widget to check
            _attr: The attribute that should have been set
            value: The value that the attribute have been set to.
        """
        self.assertEqual(self.pytest_assert(attribute_value, _widget, _attr), value)

    def assertValuesSet(self, _widget, _attr, values):
        """Assert that the widget implementation has been set to multiple
        values.

        Args:
            _widget: The interface of the widget to check
            _attr: The attribute that should have been set
            value: The values that the attribute have been set to.
        """
        self.assertEqual(self.pytest_assert(attribute_values, _widget, _attr), values)

    def assertValueGet(self, _widget, _attr):
        """Assert that the widget implementation attempted to retrieve an
        attribute.

        Args:
            _widget: The interface of the widget to check
            _attr: The attribute that should have been retrieved
        """
        self.pytest_assert(assert_attribute_retrieved, _widget, _attr)

    def assertValueNotGet(self, _widget, _attr):
        self.pytest_assert(assert_attribute_not_retrieved, _widget, _attr)

    def assertValueNotSet(self, _widget, _attr):
        self.pytest_assert(assert_attribute_not_set, _widget, _attr)

    def assertActionNotPerformed(self, _widget, _action):
        """Assert that the named action was *not* performed by a widget.

        Args:
            _widget: The interface of the widget that should not have performed the action.
            _action: The name of the action to check
        """
        self.pytest_assert(assert_action_not_performed, _widget, _action)

    def assertActionPerformed(self, _widget, _action):
        """Assert that the named action performed by a widget.
        Args:
            _widget: The interface of the widget that should have performed the action.
            _action: The name of the action to check
        """
        self.pytest_assert(assert_action_performed, _widget, _action)

    def assertActionPerformedWith(self, _widget, _action, **test_data):
        """Was the action performed with specific test data.

        Args:
            _widget: The interface of the widget that should have performed the action.
            _action: The name of the action to check.
            **test_data: The arguments that should have been passed to the action.

        Returns:
            If a matching action was performed, the full data of
            the performed action if. False otherwise.
        """
        self.pytest_assert(assert_action_performed_with, _widget, _action, **test_data)
