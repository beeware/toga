import sys
import unittest

from travertino.declaration import BaseStyle
from travertino.layout import BaseBox
from travertino.size import BaseIntrinsicSize


def not_required(method_or_class):
    """ This decorator function is used to mark methods or classes
    that they are not required for interface compliance.

    Args:
        method_or_class: The method or class to decorate

    Returns:
        The method or class being decorated
    """
    return method_or_class


def not_required_on(*args):
    """ This decorator function is used to mark methods or classes
    that they are not required on certain platforms.
    This is only used by the implementation checks creation mechanism.

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
    """A base class for objects on the dummy backend whose activity will be logged.

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
        """Record that an action was performed on the object

        Args:
            action: The action that was performed
            data: Any data associated with the action.
        """
        sequence = EventLog.log(EventLog.ACTION, instance=self, action=action, **data)
        self._actions.setdefault(action, {})[sequence] = data


_MODULES = {}


def log_action(module, action, **data):
    """Record that an action function was invoked

    Args:
        action: The action that was performed
        data: Any data associated with the action.
    """
    _MODULES.setdefault(module, LoggedObject())._action(action, **data)


class TestStyle(BaseStyle):
    class IntrinsicSize(BaseIntrinsicSize):
        pass

    class Box(BaseBox):
        pass

    def layout(self, root, viewport):
        pass


class TestCase(unittest.TestCase):
    def setUp(self):
        EventLog.reset()
        # We use the existence of a __main__ module as a proxy for being in test
        # conditions. This isn't *great*, but the __main__ module isn't meaningful
        # during tests, and removing it allows us to avoid having explicit "if
        # under test conditions" checks in paths.py.
        if '__main__' in sys.modules:
            del sys.modules['__main__']

    def reset_event_log(self):
        EventLog.reset()

    def assertFunctionNotPerformed(self, _module, action):
        """Assert that the action function from module was *not* performed.

        Args:
            _module: The module with the action that should not have been performed.
            action: The name of the action to check

        """
        try:
            self.assertNotIn(
                action,
                _MODULES[_module]._actions,
                'Action {} unexpectedly performed by {}.'.format(action, _module)
            )
        except AttributeError:
            self.fail('Module {} is not a logged object'.format(_module))

    def assertFunctionPerformed(self, _module, action):
        """Assert that the action function from module was performed.

        Args:
            _module: The module with the action that should have been performed.
            action: The name of the action to check

        """
        try:
            self.assertIn(
                action,
                _MODULES[_module]._actions,
                'Action {} from {} not performed. Actions were: {}'.format(
                    action,
                    _module,
                    sorted(_MODULES[_module]._actions.keys())
                )
            )
        except AttributeError:
            self.fail('Module {} is not a logged object'.format(_module))

    def assertFunctionPerformedWith(self, _module, action, **test_data):
        """Confirm that the action function form module was performed with specific test data

        Args:
            _module: The module with the action function that should have been performed.
            action: The name of the action to check.
            **test_data: The arguments that should have been passed to the action.

        Returns:
            If a matching action was performed, the full data of
            the performed action if. False otherwise.
        """
        try:
            found = True
            # Iterate over every action that was performed on
            # this object.
            for sequence, data in _MODULES[_module]._actions[action].items():
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
                # for the test data. Otherwise, reset, and try again
                # with the next recorded action.
                if found:
                    return data
                else:
                    found = True

            # None of the recorded actions match the test data.
            self.fail('Action {} not performed by {} with {}. Actions were: {}'.format(
                    action,
                    _module,
                    test_data,
                    sorted(_MODULES[_module]._actions[action].items())
                ))
        except KeyError:
            # The action wasn't performed
            self.fail('Action {} not performed by {}. Actions were: {}'.format(
                    action,
                    _module,
                    sorted(_MODULES[_module]._actions.keys())
                ))
        except AttributeError:
            self.fail('Widget {} is not a logged object'.format(_module))

#####

    def assertValueSet(self, _widget, attr, value):
        """Assert that the widget implementation has set an attribute to a value.

        Args:
            _widget: The interface of the widget to check
            attr: The attribute that should have been set
            value: The value that the attribute have been set to.
        """
        try:
            self.assertEqual(
                _widget._impl._sets[attr][-1],
                value,
                'Widget {} has not had attribute {!r} set to {!r}; got {!r}.'.format(
                    _widget,
                    attr,
                    value,
                    _widget._impl._sets[attr][-1]
                )
            )
        except KeyError:
            self.fail('Widget {} did not have the attribute {!r} set; set attributes were {}.'.format(
                _widget,
                attr,
                ', '.join('{!r}'.format(a) for a in sorted(_widget._impl._sets.keys()))
            ))
        except AttributeError:
            self.fail('Widget {} is not a logged object'.format(_widget))

    def assertValuesSet(self, _widget, attr, values):
        """Assert that the widget implementation has been set to multiple values.

        Args:
            _widget: The interface of the widget to check
            attr: The attribute that should have been set
            value: The values that the attribute have been set to.
        """
        try:
            self.assertEqual(
                _widget._impl._sets[attr],
                values,
                'Widget {} has not had attribute {!r} set to the values {}; got {}.'.format(
                    _widget,
                    attr,
                    ', '.join('{!r}'.format(v) for v in values),
                    ', '.join('{!r}'.format(v) for v in _widget._impl._sets[attr])
                )
            )
        except KeyError:
            self.fail('Widget {} did not have the attribute {!r} set; set attributes were {}.'.format(
                _widget,
                attr,
                ','.join('{!r}'.format(a) for a in sorted(_widget._impl._sets.keys()))
            ))
        except AttributeError:
            self.fail('Widget {} is not a logged object'.format(_widget))

    def assertValueGet(self, _widget, attr):
        """Assert that the widget implementation attempted to retrieve an attribute

        Args:
            _widget: The interface of the widget to check
            attr: The attribute that should have been retrieved
        """
        try:
            self.assertIn(
                attr,
                _widget._impl._gets,
                'Widget {} did not retrieve the attribute {!r}; retrieved attributes were {}.'.format(
                    _widget,
                    attr,
                    ','.join(
                        '{!r}'.format(a) for a in sorted(_widget._impl._gets)
                    )
                )
            )
        except AttributeError:
            self.fail('Widget {} is not a logged object'.format(_widget))

    def assertValueNotGet(self, _widget, attr):
        self.assertTrue(
            attr not in _widget._impl._gets,
            msg="Expected {attr} not to be get, but it was.".format(attr=attr)
        )

    def assertValueNotSet(self, _widget, attr):
        self.assertTrue(
            attr not in _widget._impl._sets,
            msg="Expected {attr} not to be set, but it was.".format(attr=attr)
        )

    def assertActionNotPerformed(self, _widget, action):
        """Assert that the named action was *not* performed by a widget.

        Args:
            _widget: The interface of the widget that should not have performed the action.
            action: The name of the action to check

        """
        try:
            self.assertNotIn(
                action,
                _widget._impl._actions,
                'Action {} unexpectedly performed by {}.'.format(action, _widget)
            )
        except AttributeError:
            self.fail('Widget {} is not a logged object'.format(_widget))

    def assertActionPerformed(self, _widget, action):
        """Assert that the named action performed by a widget.

        Args:
            _widget: The interface of the widget that should have performed the action.
            action: The name of the action to check

        """
        try:
            self.assertIn(
                action,
                _widget._impl._actions,
                'Action {} not performed by {}. Actions were: {}'.format(
                    action,
                    _widget,
                    sorted(_widget._impl._actions.keys())
                )
            )
        except AttributeError:
            self.fail('Widget {} is not a logged object'.format(_widget))

    def assertActionPerformedWith(self, _widget, action, **test_data):
        """Was the action performed with specific test data

        Args:
            _widget: The interface of the widget that should have performed the action.
            action: The name of the action to check.
            **test_data: The arguments that should have been passed to the action.

        Returns:
            If a matching action was performed, the full data of
            the performed action if. False otherwise.
        """
        try:
            found = True
            # Iterate over every action that was performed on
            # this object.
            for sequence, data in _widget._impl._actions[action].items():
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
                # for the test data. Otherwise, reset, and try again
                # with the next recorded action.
                if found:
                    return data
                else:
                    found = True

            # None of the recorded actions match the test data.
            self.fail('Action {} not performed by {} with {}. Actions were: {}'.format(
                    action,
                    _widget,
                    test_data,
                    sorted(_widget._impl._actions[action].items())
                ))
        except KeyError:
            # The action wasn't performed
            self.fail('Action {} not performed by {}. Actions were: {}'.format(
                    action,
                    _widget,
                    sorted(_widget._impl._actions.keys())
                ))
        except AttributeError:
            self.fail('Widget {} is not a logged object'.format(_widget))
