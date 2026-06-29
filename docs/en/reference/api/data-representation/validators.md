{{ component_header("Validators") }}

## Usage

A validator is a callable that accepts a string as input, and returns `None` on success, or a string on failure. If a string is returned, that string will be used as an error message. For example, the following example will validate that the user's input starts with the text "Hello":

```python
def must_say_hello(value):
    if value.lower().startswith("hello"):
        return None
    return "Why didn't you say hello?"
```

Toga provides built-in validators for a range of common validation types, as well as some base classes that can be used as a starting point for custom validators.

A list of validators can then be provided to any widget that performs validation, such as the [`TextInput`][toga.TextInput] widget. In the following example, a `TextInput` will validate that the user has entered text that starts with "hello", and has provided at least 10 characters of input:

```python
import toga
from toga.validators import MinLength

widget = toga.TextInput(validators=[
    must_say_hello,
    MinLength(10)
])
```

Whenever the input changes, all validators will be evaluated in the order they have been specified. The first validator to fail will put the widget into an "error" state, and the error message returned by that validator will be displayed to the user.

## Reference

::: toga.validators.BooleanValidator

::: toga.validators.CountValidator

::: toga.validators.Contains

::: toga.validators.ContainsDigit

::: toga.validators.ContainsLowercase

::: toga.validators.ContainsSpecial

::: toga.validators.ContainsUppercase

::: toga.validators.Email

::: toga.validators.EndsWith

::: toga.validators.Integer

::: toga.validators.LengthBetween

::: toga.validators.MatchRegex

::: toga.validators.MaxLength

::: toga.validators.MinLength

::: toga.validators.NotContains

::: toga.validators.Number

::: toga.validators.StartsWith
