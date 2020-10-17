import re
from typing import Optional, Union, List, Callable
from string import ascii_uppercase, ascii_lowercase, digits

INTEGER_REGEX = r"^[0-9]+$"
NUMBER_REGEX = r"^[-]?(\d+|\d*\.\d+|\d+.\d*)$"
EMAIL_REGEX = (
    r"^[a-zA-Z][a-zA-Z0-9\.]*[a-zA-Z0-9]@[a-zA-Z][a-zA-Z0-9]*(\.[a-zA-Z0-9]+)+$"
)


def min_length(length: int, error_message: Optional[str] = None):
    if error_message is None:
        error_message = "Input is too short (length should be at least {})".format(
            length
        )
    return __build_boolean_validator(
        is_valid_method=lambda a: len(a) >= length, error_message=error_message
    )


def max_length(length: int, error_message: Optional[str] = None):
    if error_message is None:
        error_message = "Input is too long (length should be at most {})".format(length)
    return __build_boolean_validator(
        is_valid_method=lambda a: len(a) <= length, error_message=error_message
    )


def length_between(min_value: int, max_value: int, error_message: Optional[str] = None):
    return combine(
        min_length(min_value, error_message=error_message),
        max_length(max_value, error_message=error_message),
    )


def contains(
    substrings: Union[str, List[str]],
    count: Optional[int] = None,
    error_message: Optional[str] = None,
):
    if isinstance(substrings, str):
        substrings = [substrings]

    if error_message is not None:
        expected_non_existence = expected_count = expected_existence = error_message
    else:
        if len(substrings) == 1:
            substrings_string = '"{}"'.format(substrings[0])
        else:
            substrings_string = ", ".join(
                '"{}"'.format(substring) for substring in substrings[:-1]
            ) + ' or "{}"'.format(substrings[-1])
        expected_existence = "Input should contain {}".format(substrings_string)
        expected_non_existence = "Input should not contain {}".format(substrings_string)
        expected_count = "Input should contain {} exactly {} times".format(
            substrings_string, count
        )

    return __build_count_validator(
        count_method=lambda a: sum(a.count(substring) for substring in substrings),
        count=count,
        expected_existence=expected_existence,
        expected_non_existence=expected_non_existence,
        expected_count=expected_count,
    )


def not_contains(substring: str, error_message: Optional[str] = None):
    return contains(substring, count=0, error_message=error_message)


def match_regex(regex_string, error_message: Optional[str] = None):
    if error_message is None:
        error_message = "Input should match regex: {}".format(regex_string)
    return __build_boolean_validator(
        is_valid_method=lambda a: bool(re.search(regex_string, a)),
        error_message=error_message,
    )


def contains_uppercase(
    count: Optional[int] = None, error_message: Optional[str] = None
):
    if error_message is not None:
        expected_non_existence = expected_count = expected_existence = error_message
    else:
        expected_existence = "Input should contain at least one uppercase character"
        expected_non_existence = "Input should not contain uppercase characters"
        expected_count = "Input should contain exactly {} uppercase characters".format(
            count
        )

    return __build_count_validator(
        count_method=lambda a: len([char for char in a if char in ascii_uppercase]),
        count=count,
        expected_existence=expected_existence,
        expected_non_existence=expected_non_existence,
        expected_count=expected_count,
    )


def contains_lowercase(
    count: Optional[int] = None, error_message: Optional[str] = None
):
    if error_message is not None:
        expected_non_existence = expected_count = expected_existence = error_message
    else:
        expected_existence = "Input should contain at least one lowercase character"
        expected_non_existence = "Input should not contain lowercase characters"
        expected_count = "Input should contain exactly {} lowercase characters".format(
            count
        )

    return __build_count_validator(
        count_method=lambda a: len([char for char in a if char in ascii_lowercase]),
        count=count,
        expected_existence=expected_existence,
        expected_non_existence=expected_non_existence,
        expected_count=expected_count,
    )


def contains_digit(count: Optional[int] = None, error_message: Optional[str] = None):
    if error_message is not None:
        expected_non_existence = expected_count = expected_existence = error_message
    else:
        expected_existence = "Input should contain at least one digit"
        expected_non_existence = "Input should not contain digits"
        expected_count = "Input should contain exactly {} digits".format(count)

    return __build_count_validator(
        count_method=lambda a: len([char for char in a if char in digits]),
        count=count,
        expected_existence=expected_existence,
        expected_non_existence=expected_non_existence,
        expected_count=expected_count,
    )


def contains_special(count: Optional[int] = None, error_message: Optional[str] = None):
    if error_message is not None:
        expected_non_existence = expected_count = expected_existence = error_message
    else:
        expected_existence = "Input should contain at least one special character"
        expected_non_existence = "Input should not contain specials characters"
        expected_count = "Input should contain exactly {} special characters".format(
            count
        )

    return __build_count_validator(
        count_method=lambda a: len(
            [char for char in a if not char.isalpha() and not char.isdigit()]
        ),
        count=count,
        expected_existence=expected_existence,
        expected_non_existence=expected_non_existence,
        expected_count=expected_count,
    )


def integer(error_message: Optional[str] = None):
    if error_message is None:
        error_message = "Input should be an integer"
    return match_regex(INTEGER_REGEX, error_message=error_message)


def number(error_message: Optional[str] = None):
    if error_message is None:
        error_message = "Input should be a number"
    return match_regex(NUMBER_REGEX, error_message=error_message)


def email(error_message: Optional[str] = None):
    if error_message is None:
        error_message = "Input should be a valid email address"
    return match_regex(
        EMAIL_REGEX,
        error_message=error_message)


def combine(*validators):
    """Use this method to combine multiple validators."""

    def combined_validator(input_string):
        for validator in validators:
            error_message = validator(input_string)
            if error_message is not None:
                return error_message
        return None

    return combined_validator


def __build_boolean_validator(
    is_valid_method: Callable[[str], bool], error_message: str
):
    def validator(input_string: str):
        if not is_valid_method(input_string):
            return error_message
        return None

    return validator


def __build_count_validator(
    count_method: Callable[[str], int],
    count: Optional[int],
    expected_existence: str,
    expected_non_existence: str,
    expected_count: str,
):
    def validator(input_string: str):
        actual_count = count_method(input_string)
        if actual_count == 0 and count != 0:
            return expected_existence
        if actual_count != 0 and count == 0:
            return expected_non_existence
        if count is not None and actual_count != count:
            return expected_count
        return None

    return validator
