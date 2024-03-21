import pytest

from toga import validators


@pytest.mark.parametrize(
    "value, kwargs, error",
    [
        # Exact minimum size
        ("exact", dict(length=5), None),
        # Exceeds minimum size
        ("this is a long string", dict(length=5), None),
        # Allow empty strings
        ("", dict(length=5), None),
        # Too short
        (
            "bad!",
            dict(length=5),
            "Input is too short (length should be at least 5)",
        ),
        # Too short, different length
        (
            "this is a long string",
            dict(length=25),
            "Input is too short (length should be at least 25)",
        ),
        # Custom error message
        (
            "bad",
            dict(length=5, error_message="Badness"),
            "Badness",
        ),
        # Don't allow empty strings
        (
            "",
            dict(length=5, allow_empty=False),
            "Input is too short (length should be at least 5)",
        ),
    ],
)
def test_min_length(value, kwargs, error):
    validator = validators.MinLength(**kwargs)

    assert validator(value) == error


@pytest.mark.parametrize(
    "value, kwargs, error",
    [
        # Exact max size
        ("right size", dict(length=10), None),
        # Less than max size
        ("valid", dict(length=10), None),
        # Empty strings are less than any max length
        ("", dict(length=10), None),
        # Just exceeds maximum length
        (
            "bad size!!!",
            dict(length=10),
            "Input is too long (length should be at most 10)",
        ),
        # Exceeds maximum length
        (
            "this is a long string",
            dict(length=10),
            "Input is too long (length should be at most 10)",
        ),
        # Exceeds a different maximum length
        (
            "this is a long string",
            dict(length=5),
            "Input is too long (length should be at most 5)",
        ),
        # Custom error message
        (
            "this is a long string",
            dict(length=10, error_message="Badness"),
            "Badness",
        ),
    ],
)
def test_max_length(value, kwargs, error):
    validator = validators.MaxLength(**kwargs)

    assert validator(value) == error


@pytest.mark.parametrize(
    "value, kwargs, error",
    [
        # Exact max size
        ("right size", dict(min_length=5, max_length=10), None),
        # Middle size
        ("all good", dict(min_length=5, max_length=10), None),
        # Exact min size
        ("valid", dict(min_length=5, max_length=10), None),
        # Allow empty strings
        ("", dict(min_length=5, max_length=10), None),
        # Just Exceeds maximum length
        (
            "bad size!!!",
            dict(min_length=5, max_length=10),
            "Input should be between 5 and 10 characters",
        ),
        # Just less than minimum length
        (
            "bad!",
            dict(min_length=5, max_length=10),
            "Input should be between 5 and 10 characters",
        ),
        # Custom error message
        (
            "this is a long string",
            dict(min_length=5, max_length=10, error_message="Badness"),
            "Badness",
        ),
        # Don't allow empty strings
        (
            "",
            dict(min_length=5, max_length=10, allow_empty=False),
            "Input should be between 5 and 10 characters",
        ),
    ],
)
def test_length_between(value, kwargs, error):
    validator = validators.LengthBetween(**kwargs)

    assert validator(value) == error


def test_invalid_range():
    """Minimum value must be less than maximum value."""
    with pytest.raises(
        ValueError,
        match=r"Minimum length cannot be less than maximum length",
    ):
        validators.LengthBetween(min_length=10, max_length=5)


@pytest.mark.parametrize(
    "value, kwargs, error",
    [
        # Exact match
        ("hello", dict(substring="hello"), None),
        # Starts with match
        ("hello world", dict(substring="hello"), None),
        # Allow empty strings
        ("", dict(substring="hello"), None),
        # Doesn't start with match
        (
            "bad string",
            dict(substring="hello"),
            "Input should start with 'hello'",
        ),
        # Custom error message
        (
            "bad string",
            dict(substring="hello", error_message="Badness"),
            "Badness",
        ),
        # Don't allow empty strings
        (
            "",
            dict(substring="hello", allow_empty=False),
            "Input should start with 'hello'",
        ),
    ],
)
def test_startswith(value, kwargs, error):
    validator = validators.StartsWith(**kwargs)

    assert validator(value) == error


@pytest.mark.parametrize(
    "value, kwargs, error",
    [
        # Exact match
        ("goodbye", dict(substring="goodbye"), None),
        # Ends with match
        ("the final goodbye", dict(substring="goodbye"), None),
        # Allow empty strings
        ("", dict(substring="goodbye"), None),
        # Doesn't end with match
        (
            "bad string",
            dict(substring="goodbye"),
            "Input should end with 'goodbye'",
        ),
        # Custom error message
        (
            "bad string",
            dict(substring="goodbye", error_message="Badness"),
            "Badness",
        ),
        # Don't allow empty strings
        (
            "",
            dict(substring="goodbye", allow_empty=False),
            "Input should end with 'goodbye'",
        ),
    ],
)
def test_endswith(value, kwargs, error):
    validator = validators.EndsWith(**kwargs)

    assert validator(value) == error


@pytest.mark.parametrize(
    "value, kwargs, error",
    [
        # Exact single match
        ("hello", dict(substring="hello"), None),
        # Starts with match
        ("hello is what you should say", dict(substring="hello"), None),
        # Ends with match
        ("You should say hello", dict(substring="hello"), None),
        # Contains substring
        ("Say hello, you fool", dict(substring="hello"), None),
        # Contains multiple examples of substring
        ("Say hello, and hello again", dict(substring="hello"), None),
        # Contains exact match of multiple substrings
        ("Say hello, and hello again", dict(substring="hello", count=2), None),
        # Count of 0 validates non-existence
        ("Say hello, and hello again", dict(substring="bad", count=0), None),
        # Allow empty strings
        ("", dict(substring="hello"), None),
        # Doesn't contain match
        (
            "bad string",
            dict(substring="hello"),
            "Input should contain 'hello'",
        ),
        # Contain match with a count of 0
        (
            "hello world",
            dict(substring="hello", count=0),
            "Input should not contain 'hello'",
        ),
        # Contain match, but not the right count
        (
            "hello world",
            dict(substring="hello", count=2),
            "Input should contain 'hello' exactly 2 times",
        ),
        # Custom error message
        (
            "bad string",
            dict(substring="hello", error_message="Badness"),
            "Badness",
        ),
        # Don't allow empty strings
        (
            "",
            dict(substring="hello", allow_empty=False),
            "Input should contain 'hello'",
        ),
    ],
)
def test_contains(value, kwargs, error):
    validator = validators.Contains(**kwargs)

    assert validator(value) == error


@pytest.mark.parametrize(
    "value, kwargs, error",
    [
        # No match
        ("nothing to see", dict(substring="hello"), None),
        # Allow empty strings (an empty string can't contain a substring)
        ("", dict(substring="hello"), None),
        # Starts with match
        (
            "hello is what you should say",
            dict(substring="hello"),
            "Input should not contain 'hello'",
        ),
        # Ends with match
        (
            "You should say hello",
            dict(substring="hello"),
            "Input should not contain 'hello'",
        ),
        # Contains substring
        (
            "Say hello, you fool",
            dict(substring="hello"),
            "Input should not contain 'hello'",
        ),
        # Custom error message
        (
            "You should say hello",
            dict(substring="hello", error_message="Badness"),
            "Badness",
        ),
    ],
)
def test_not_contains(value, kwargs, error):
    validator = validators.NotContains(**kwargs)

    assert validator(value) == error


# Test regex matches 1 upper case, 2 lower case, then 1 upper case.
TEST_REGEX = r"[A-Z]{1}[a-z]{2}[A-Z]{1}"


@pytest.mark.parametrize(
    "value, kwargs, error",
    [
        # Exact match
        ("GooD", dict(regex_string=TEST_REGEX), None),
        # Match at start
        ("GooD is what this is", dict(regex_string=TEST_REGEX), None),
        # Match at end
        ("This is also GooD", dict(regex_string=TEST_REGEX), None),
        # Exact match in the middle of the string
        ("it's GooD if it's in the middle", dict(regex_string=TEST_REGEX), None),
        # Allow empty strings
        ("", dict(regex_string=TEST_REGEX), None),
        # Doesn't match
        (
            "no match here",
            dict(regex_string=TEST_REGEX),
            "Input should match regex: '[A-Z]{1}[a-z]{2}[A-Z]{1}'",
        ),
        # Custom error message
        (
            "no match here",
            dict(regex_string=TEST_REGEX, error_message="Badness"),
            "Badness",
        ),
        # Don't allow empty strings
        (
            "",
            dict(regex_string=TEST_REGEX, allow_empty=False),
            "Input should match regex: '[A-Z]{1}[a-z]{2}[A-Z]{1}'",
        ),
    ],
)
def test_regex(value, kwargs, error):
    validator = validators.MatchRegex(**kwargs)

    assert validator(value) == error


@pytest.mark.parametrize(
    "value, kwargs, error",
    [
        # Only uppercase
        ("GOOD!1", dict(), None),
        # Some uppercase
        ("Good!1", dict(), None),
        # Some uppercase
        ("GooD!1", dict(count=2), None),
        # Count of 0
        ("good!1", dict(count=0), None),
        # Allow empty strings
        ("", dict(), None),
        # Doesn't match
        (
            "no match here",
            dict(),
            "Input should contain at least one upper case character",
        ),
        # Bad count
        (
            "Good!1",
            dict(count=2),
            "Input should contain exactly 2 upper case characters",
        ),
        # Explicit count of 0
        (
            "Bad Text!1",
            dict(count=0),
            "Input should not contain upper case characters",
        ),
        # Custom error message
        (
            "no match here",
            dict(error_message="Badness"),
            "Badness",
        ),
        # Don't allow empty strings
        (
            "",
            dict(allow_empty=False),
            "Input should contain at least one upper case character",
        ),
    ],
)
def test_contains_uppercase(value, kwargs, error):
    validator = validators.ContainsUppercase(**kwargs)

    assert validator(value) == error


@pytest.mark.parametrize(
    "value, kwargs, error",
    [
        # Only lower case
        ("good!1", dict(), None),
        # Some lower case
        ("Good!1", dict(), None),
        # Some lower case, exact count
        ("GooD!1", dict(count=2), None),
        # Count of 0
        ("GOOD!1", dict(count=0), None),
        # Allow empty strings
        ("", dict(), None),
        # Doesn't match
        (
            "NO MATCH HERE!",
            dict(),
            "Input should contain at least one lower case character",
        ),
        # Bad count
        (
            "Good!1",
            dict(count=2),
            "Input should contain exactly 2 lower case characters",
        ),
        # Explicit count of 0
        (
            "Bad Text!1",
            dict(count=0),
            "Input should not contain lower case characters",
        ),
        # Custom error message
        (
            "NO MATCH HERE!",
            dict(error_message="Badness"),
            "Badness",
        ),
        # Don't allow empty strings
        (
            "",
            dict(allow_empty=False),
            "Input should contain at least one lower case character",
        ),
    ],
)
def test_contains_lowercase(value, kwargs, error):
    validator = validators.ContainsLowercase(**kwargs)

    assert validator(value) == error


@pytest.mark.parametrize(
    "value, kwargs, error",
    [
        # Only digits
        ("1234", dict(), None),
        # Some digits
        ("Good!12345", dict(), None),
        # Some digits, exact count
        ("GooD12!", dict(count=2), None),
        # Count of 0
        ("good!", dict(count=0), None),
        # Allow empty strings
        ("", dict(), None),
        # Doesn't match
        (
            "no match here",
            dict(),
            "Input should contain at least one digit",
        ),
        # Bad count
        (
            "Good!1",
            dict(count=2),
            "Input should contain exactly 2 digits",
        ),
        # Explicit count of 0
        (
            "Bad Text!1",
            dict(count=0),
            "Input should not contain digits",
        ),
        # Custom error message
        (
            "no match here",
            dict(error_message="Badness"),
            "Badness",
        ),
        # Don't allow empty strings
        (
            "",
            dict(allow_empty=False),
            "Input should contain at least one digit",
        ),
    ],
)
def test_contains_digit(value, kwargs, error):
    validator = validators.ContainsDigit(**kwargs)

    assert validator(value) == error


@pytest.mark.parametrize(
    "value, kwargs, error",
    [
        # Only special
        ("!@*&#^(*&!^(&@))", dict(), None),
        # Some special
        ("Good!1", dict(), None),
        # Some special, exact count
        ("GooD@!", dict(count=2), None),
        # Count of 0
        ("good1", dict(count=0), None),
        # Allow empty strings
        ("", dict(), None),
        # Doesn't match
        (
            "no match here",
            dict(),
            "Input should contain at least one special character",
        ),
        # Bad count
        (
            "Good!1",
            dict(count=2),
            "Input should contain exactly 2 special characters",
        ),
        # Explicit count of 0
        (
            "Bad Text!1",
            dict(count=0),
            "Input should not contain special characters",
        ),
        # Custom error message
        (
            "no match here",
            dict(error_message="Badness"),
            "Badness",
        ),
        # Don't allow empty strings
        (
            "",
            dict(allow_empty=False),
            "Input should contain at least one special character",
        ),
    ],
)
def test_contains_special(value, kwargs, error):
    validator = validators.ContainsSpecial(**kwargs)

    assert validator(value) == error


@pytest.mark.parametrize(
    "value, kwargs, error",
    [
        # Zero
        ("0", dict(), None),
        # positive integer
        ("123", dict(), None),
        # Negative integer
        ("-123", dict(), None),
        # Extra space
        (" 123 ", dict(), None),
        # leading zeros
        ("01234", dict(), None),
        # Allow empty strings
        ("", dict(), None),
        # Doesn't match
        (
            "no match here",
            dict(),
            "Input should be an integer",
        ),
        # Contains an integer, but not a pure integer
        (
            "no 123",
            dict(),
            "Input should be an integer",
        ),
        # Float
        (
            "1.234",
            dict(),
            "Input should be an integer",
        ),
        # Hex
        (
            "0x123",
            dict(),
            "Input should be an integer",
        ),
        # Octal
        (
            "0o123",
            dict(),
            "Input should be an integer",
        ),
        # Custom error message
        (
            "no match here",
            dict(error_message="Badness"),
            "Badness",
        ),
        # Don't allow empty strings
        (
            "",
            dict(allow_empty=False),
            "Input should be an integer",
        ),
    ],
)
def test_integer(value, kwargs, error):
    validator = validators.Integer(**kwargs)

    assert validator(value) == error


@pytest.mark.parametrize(
    "value, kwargs, error",
    [
        # Zero
        ("0", dict(), None),
        # positive integer
        ("123", dict(), None),
        # Negative integer
        ("-123", dict(), None),
        # Extra space
        (" 123 ", dict(), None),
        # leading zeros
        ("01234", dict(), None),
        # Float
        ("12.34", dict(), None),
        # Negative Float
        ("-12.34", dict(), None),
        # Float, no leading 0
        (".1234", dict(), None),
        # Negative Float, no leading 0
        ("-.1234", dict(), None),
        # Exponential
        ("1.23e+4", dict(), None),
        # Negative Exponential
        ("-1.23e-4", dict(), None),
        # Exponential (capitalized)
        ("1.23E+4", dict(), None),
        # Negative (capitalized)
        ("-1.23E-4", dict(), None),
        # Allow empty strings
        ("", dict(), None),
        # Doesn't match
        (
            "no match here",
            dict(),
            "Input should be a number",
        ),
        # Contains a number, but not a pure number
        (
            "no 1.23",
            dict(),
            "Input should be a number",
        ),
        # Just a decimal point isn't a number
        (
            ".",
            dict(),
            "Input should be a number",
        ),
        # Just an exponent isn't a number
        (
            "e+9",
            dict(),
            "Input should be a number",
        ),
        # Custom error message
        (
            "no match here",
            dict(error_message="Badness"),
            "Badness",
        ),
        # Don't allow empty strings
        (
            "",
            dict(allow_empty=False),
            "Input should be a number",
        ),
    ],
)
def test_number(value, kwargs, error):
    validator = validators.Number(**kwargs)

    assert validator(value) == error


@pytest.mark.parametrize(
    "value, kwargs, error",
    [
        # Valid email addresses
        ("tiberius@beeware.org", dict(), None),
        ("tiberius.yak@beeware.org", dict(), None),
        ("tiberius+yak@beeware.org", dict(), None),
        ("tiberius@beeware.ab.cd", dict(), None),
        ("tiberius@localhost", dict(), None),
        ("tiberius@beeware", dict(), None),
        ("2iberius@beeware.org", dict(), None),
        # Allow empty strings
        ("", dict(), None),
        # Invalid email addresses
        ("tiberius.beeware.org", dict(), "Input should be a valid email address"),
        ("tiberius@me@beeware.org", dict(), "Input should be a valid email address"),
        ("tiberius@beeware.", dict(), "Input should be a valid email address"),
        # Custom error message
        ("not an email", dict(error_message="badness"), "badness"),
        # Disallow empty strings
        ("", dict(allow_empty=False), "Input should be a valid email address"),
    ],
)
def test_email(value, kwargs, error):
    validator = validators.Email(**kwargs)

    assert validator(value) == error


# @pytest.mark.parametrize(
#     "value",
#     [
#     ],
# )
# def test_invalid_email(value):
#     validator = validators.Email()

#     assert validator(value) == "Input should be a valid email address"
