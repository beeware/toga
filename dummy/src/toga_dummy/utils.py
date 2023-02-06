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

    Args:
        method_or_class: The method or class to decorate

    Returns:
        The method or class being decorated
    """
    return method_or_class


def not_required_on(*args):
    """This decorator function is used to mark methods or classes that they are
    not required on certain platforms. This is only used by the implementation
    checks creation mechanism.

    Args:
        *args (str): Takes arguments in form of strings.
            Possible *args are 'mobile', 'desktop',
            as well as all platform names ('iOS', 'gtk', 'android' ...).

    Examples:
        >>> # Marks the function as only required on platforms that are not "mobile".
        >>> @not_required_on('mobile')
        >>> def open_window():
        >>>     self.window.open()

        >>> # Function is not required on "mobile" and "gtk" backends.
        >>> @not_required_on('mobile', 'gtk')
        >>> def open_window():
        >>>     self.window.open()

    Returns:
        The method or class being decorated
    """

    def _dec(method_or_class):
        return method_or_class

    return _dec


###########################################################################
# The event types that can be logged
###########################################################################


class EventLog:
    # Event types that can be logged
    SET_VALUE = object()
    GET_VALUE = object()
    ACTION = object()

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

        Args:
            logtype: The type of object being logged (SET_VALUE, etc)
            instance: The instance that generated loggable activity
            context: A dictionary of data related to the event. The contents
                of the dictionary will depend on the event that occurred.

        Returns:
            The sequence value of the log entry
        """
        entry = LogEntry(logtype, instance, **context)
        cls._log.append(entry)
        return entry.sequence


class LogEntry:
    """An entry in the event log.

    Args:
        logtype: The type of object being logged (SET_VALUE, etc)
        instance: The instance that generated loggable activity
        context: A dictionary of data related to the event. The contents
            of the dictionary will depend on the event that occurred.
    """

    def __init__(self, logtype, instance, **context):
        self.sequence = EventLog.next_sequence_value()
        self.logtype = logtype
        self.instance = instance
        self.context = context


class LoggedObject:
    """A base class for objects on the dummy backend whose activity will be
    logged.

    Objects specified in the dummy backend should extend this class, and
    log any activity they perform using the methods on this object.
    """

    def __init__(self):
        self._actions = {}
        self._sets = {}
        self._gets = set()

    def _set_value(self, attr, value):
        """Set a value on the dummy object.

        Logs the new value for the attribute, and tracks it in the ``_sets``
        list for the widget.

        Args:
            attr: The name of the attribute to set
            value: The new value for the attribute
        """
        EventLog.log(EventLog.SET_VALUE, instance=self, attr=attr, value=value)
        self._sets.setdefault(attr, []).append(value)

    def _get_value(self, attr, default=None):
        """Get a value on the dummy object.

        Logs the request for the attribute, and returns the value as stored on
        a local attribute.

        Args:
            attr: The name of the attribute to get
            default: The default value for the attribute if it hasn't already been set.

        Returns:
            The value of the attribute, or ``default`` if the value has not been set.
        """
        EventLog.log(EventLog.GET_VALUE, instance=self, attr=attr)
        self._gets.add(attr)
        return self._sets.get(attr, [default])[-1]

    def _action(self, action, **data):
        """Record that an action was performed on the object.

        Args:
            action: The action that was performed
            data: Any data associated with the action.
        """
        sequence = EventLog.log(EventLog.ACTION, instance=self, action=action, **data)
        self._actions.setdefault(action, {})[sequence] = data


_MODULES = {}


def log_action(module, action, **data):
    """Record that an module level action was invoked.

    :param action: The action that was performed
    :param data: Any data associated with the action.
    """
    _MODULES.setdefault(module, LoggedObject())._action(action, **data)


class TestStyle(BaseStyle):
    class IntrinsicSize(BaseIntrinsicSize):
        pass

    class Box(BaseBox):
        pass

    def layout(self, root, viewport):
        pass


###########################################################################
# Pytest widget assertion helpers
###############################################################################


def assert_module_action_not_performed(_module, _action):
    """Assert that the module-level action was *not* performed.

    :param _module: The module with the action that should not have been performed.
    :param _action: The name of the action to check
    :returns: True if the action was not performed.
    """
    try:
        assert not (
            _action in _MODULES[_module]._actions
        ), f"Action {_action!r} unexpectedly performed by {_module}."
    except AttributeError:
        pytest.fail(f"Module {_module} is not a logged object")


def assert_module_action_performed(_module, _action):
    """Assert that a module-level action was performed.

    :param _module: The module with the action that should have been performed.
    :param _action: The name of the action to check
    :returns: True if the action was performed
    """
    try:
        assert _action in _MODULES[_module]._actions, (
            f"Action {_action!r} from {_module} not performed. "
            f"Actions were: {sorted(_MODULES[_module]._actions.keys())}"
        )
    except AttributeError:
        pytest.fail(f"Module {_module} is not a logged object")


def assert_module_action_performed_with(_module, _action, **test_data):
    """Assert if the module-level action was performed with specific test data.

    :param _module: The module with the action that should have been performed.
    :param _action: The name of the action to check
    :param test_data: The arguments that should have been passed to the action.
    :returns: True if a matching action was performed.
    """
    try:
        # Iterate over every action that was performed on
        # this object.
        for _, data in _MODULES[_module]._actions[_action].items():
            found = True
            # Iterate over every key and value in the test
            # data. If the value in the recorded action
            # doesn't match the requested value, then this isn't
            # a match.
            for key, value in test_data.items():
                try:
                    if data[key] != value:
                        found = False
                except KeyError:
                    found = False

            # Default behavior is to be found; so if we're
            # still in a "found" state, this action is a match
            # for the test data. Otherwise, try again
            # with the next recorded action.
            if found:
                return

        # None of the recorded actions match the test data.
        actual_actions = sorted(_MODULES[_module]._actions.keys())
        pytest.fail(
            f"Action {_action!r} not performed by {_module} with {test_data}. "
            f"Actions were: {actual_actions}"
        )
    except KeyError:
        # The action wasn't performed
        actual_actions = sorted(_MODULES[_module]._actions.keys())
        pytest.fail(
            f"Action {_action!r} not performed by {_module}. "
            f"Actions were: {actual_actions}"
        )
    except AttributeError:
        pytest.fail(f"Module {_module} is not a logged object")


def attribute_value(_widget, _attr):
    """Retrieve the current value of a widget property.

    :param _widget: The interface of the widget to check
    :param _attr: The attribute to retrieve.
    :returns: The current value of the attribute
    """
    try:
        return _widget._impl._sets[_attr][-1]
    except KeyError:
        set_attributes = ", ".join(f"{a!r}" for a in sorted(_widget._impl._sets.keys()))
        pytest.fail(
            f"Widget {_widget} did not have the attribute {_attr!r} set; "
            f"set attributes were {set_attributes}."
        )
    except AttributeError:
        pytest.fail(f"Widget {_widget} is not a logged object")


def attribute_values(_widget, _attr):
    """Retrieve the list of values that the property has been set to.

    :param _widget: The interface of the widget to check
    :param _attr: The attribute to retrieve.
    :returns: The list of values to which the attribute has been set.
    """
    try:
        return _widget._impl._sets[_attr]
    except KeyError:
        known_attributes = ",".join(
            f"{a!r}" for a in sorted(_widget._impl._sets.keys())
        )
        pytest.fail(
            f"Widget {_widget} did not have the attribute {_attr!r} set; "
            f"known attributes were {known_attributes}."
        )
    except AttributeError:
        pytest.fail(f"Widget {_widget} is not a logged object")


def assert_attribute_retrieved(_widget, _attr):
    """Assert that the widget implementation attempted to retrieve an attribute.

    :param _widget: The interface of the widget to check
    :param _attr: The attribute to check.
    :returns: True if the attribute was retrieved
    """
    try:
        known_attributes = ",".join(f"{a!r}" for a in sorted(_widget._impl._gets))
        assert _attr in _widget._impl._gets, (
            f"Widget {_widget} did not retrieve the attribute {_attr!r}; "
            f"retrieved attributes were {known_attributes}."
        )
    except AttributeError:
        pytest.fail(f"Widget {_widget} is not a logged object")


def assert_attribute_not_retrieved(_widget, _attr):
    """Assert that the widget implementation did not attempt to retrieve an attribute.

    :param _widget: The interface of the widget to check
    :param _attr: The attribute to check.
    :returns: True if the
    """
    try:
        assert (
            _attr not in _widget._impl._gets
        ), f"Widget {_widget} unexpectedly retrieved the attribute {_attr!r}."
    except AttributeError:
        pytest.fail(f"Widget {_widget} is not a logged object")


def assert_attribute_not_set(_widget, _attr):
    """Assert that the widget implementation did not attempt to set an attribute.

    :param _widget: The interface of the widget to check
    :param _attr: The attribute to check.
    :returns: True if the attribute was not set
    """
    try:
        assert (
            _attr not in _widget._impl._sets
        ), f"Widget {_widget} unexpectedly set the attribute {_attr!r}."
    except AttributeError:
        pytest.fail(f"Widget {_widget} is not a logged object")


def assert_action_not_performed(_widget, _action):
    """Assert that the named action was *not* performed by a widget.

    :param _widget: The interface of the widget to check
    :param _action: The action to check.
    :returns: True if the action was not performed
    """
    try:
        assert (
            _action not in _widget._impl._actions
        ), f"Action {_action!r} unexpectedly performed by {_widget}."
    except AttributeError:
        pytest.fail(f"Widget {_widget} is not a logged object")


def assert_action_performed(_widget, _action):
    """Assert that the named action was performed by a widget.

    :param _widget: The interface of the widget to check
    :param _action: The action to check.
    :returns: True if the action was performed
    """
    try:
        assert _action in _widget._impl._actions, (
            f"Action {_action!r} not performed by {_widget}. "
            f"Actions were: {sorted(_widget._impl._actions.keys())}"
        )
    except AttributeError:
        pytest.fail(f"Widget {_widget} is not a logged object")


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
        for _, data in _widget._impl._actions[_action].items():
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

        # None of the recorded actions match the test data.
        pytest.fail(
            f"Action {_action!r} not performed by {_widget} with {test_data}. "
            f"Actions were: {sorted(_widget._impl._actions[_action].items())}"
        )
    except KeyError:
        # The action wasn't performed
        pytest.fail(
            f"Action {_action!r} not performed by {_widget}. "
            f"Actions were: {sorted(_widget._impl._actions.keys())}"
        )
    except AttributeError:
        pytest.fail(f"Widget {_widget} is not a logged object")


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

    def assertFunctionNotPerformed(self, _module, _action):
        """Assert that the action function from module was *not* performed.

        Args:
            _module: The module with the action that should not have been performed.
            _action: The name of the action to check
        """
        self.pytest_assert(assert_module_action_not_performed, _module, _action)

    def assertFunctionPerformed(self, _module, _action):
        """Assert that the action function from module was performed.

        Args:
            _module: The module with the action that should have been performed.
            _action: The name of the action to check
        """
        self.pytest_assert(assert_module_action_performed, _module, _action)

    def assertFunctionPerformedWith(self, _module, _action, **test_data):
        """Confirm that the action function form module was performed with
        specific test data.

        Args:
            _module: The module with the action function that should have been performed.
            action: The name of the action to check.
            **test_data: The arguments that should have been passed to the action.

        Returns:
            If a matching action was performed, the full data of
            the performed action if. False otherwise.
        """
        self.pytest_assert(
            assert_module_action_performed_with, _module, _action, **test_data
        )

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
