.. _validators:

Validators
==========

A mechanism for validating that input meets a given set of criteria.

Usage
-----

A validator is a callable that accepts a string as input, and returns ``None``
on success, or a string on failure. If a string is returned, that string will be
used as an error message. For example, the following example will validate that
the user's input starts with the text "Hello":

.. code-block:: python

    def must_say_hello(value):
        if value.lower().startswith("hello"):
            return None
        return "Why didn't you say hello?"

Toga provides built-in validators for a range of common validation types, as well
as some base classes that can be used as a starting point for custom validators.

A list of validators can then be provided to any widget that performs validation, such
as the :class:`~toga.TextInput` widget. In the following example, a ``TextInput`` will
validate that the user has entered text that starts with "hello", and has provided at
least 10 characters of input:

.. code-block:: python

    import toga
    from toga.validators import MinLength

    widget = toga.TextInput(validators=[
        must_say_hello,
        MinLength(10)
    ])

Whenever the input changes, all validators will be evaluated in the order they
have been specified. The first validator to fail will put the widget into an
"error" state, and the error message returned by that validator will be
displayed to the user.

Reference
---------

.. automodule:: toga.validators
