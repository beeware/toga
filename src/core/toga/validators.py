import re
from typing import Optional, Union, List, Callable
from string import ascii_uppercase, ascii_lowercase, digits


class BooleanValidator:

    def __init__(
        self,
        error_message: str,
        allow_empty: bool = True
    ):
        self.error_message = error_message
        self.allow_empty = allow_empty

    def __call__(self, input_string: str):
        if self.allow_empty and input_string == "":
            return None
        return None if self.is_valid(input_string) else self.error_message

    def is_valid(self, input_string: str):
        raise NotImplementedError(
            "is_valid is not implemented in BooleanValidator. "
            "Please override it."
        )


class CountValidator:

    def __init__(
        self,
        count_method: Callable[[str], int],
        count: Optional[int],
        expected_existence: str,
        expected_non_existence: str,
        expected_count: str,
        allow_empty: bool = True,
    ):
        self.count_method = count_method
        self.count = count
        self.expected_existence = expected_existence
        self.expected_non_existence = expected_non_existence
        self.expected_count = expected_count
        self.allow_empty = allow_empty

    def __call__(self, input_string: str):
        if self.allow_empty and input_string == "":
            return None
        actual_count = self.count_method(input_string)
        if actual_count == 0 and self.count != 0:
            return self.expected_existence
        if actual_count != 0 and self.count == 0:
            return self.expected_non_existence
        if self.count is not None and actual_count != self.count:
            return self.expected_count
        return None


class MinLength(BooleanValidator):

    def __init__(
        self,
        length: int,
        error_message: Optional[str] = None,
        allow_empty: bool = True
    ):
        if error_message is None:
            error_message = "Input is too short (length should be at least {})".format(
                length
            )
        super().__init__(error_message=error_message, allow_empty=allow_empty)
        self.length = length

    def is_valid(self, input_string: str):
        return len(input_string) >= self.length


class MaxLength(BooleanValidator):

    def __init__(
        self,
        length: int,
        error_message: Optional[str] = None,
        allow_empty: bool = True
    ):
        if error_message is None:
            error_message = "Input is too long (length should be at most {})".format(
                length
            )
        super().__init__(error_message=error_message, allow_empty=allow_empty)
        self.length = length

    def is_valid(self, input_string: str):
        return len(input_string) <= self.length


def length_between(
    min_value: int,
    max_value: int,
    error_message: Optional[str] = None,
    allow_empty: bool = True,
):
    return combine(
        MinLength(min_value, error_message=error_message, allow_empty=allow_empty),
        MaxLength(max_value, error_message=error_message, allow_empty=allow_empty),
    )


class StartsWith(BooleanValidator):

    def __init__(
        self,
        substring: str,
        error_message: Optional[str] = None,
        allow_empty: bool = True,
    ):
        if error_message is None:
            error_message = 'Input should start with "{}"'.format(substring)

        super().__init__(error_message=error_message, allow_empty=allow_empty)
        self.substring = substring

    def is_valid(self, input_string: str):
        return input_string.startswith(self.substring)


class EndsWith(BooleanValidator):

    def __init__(
        self,
        substring: str,
        error_message: Optional[str] = None,
        allow_empty: bool = True,
    ):
        if error_message is None:
            error_message = 'Input should end with "{}"'.format(substring)

        super().__init__(error_message=error_message, allow_empty=allow_empty)
        self.substring = substring

    def is_valid(self, input_string: str):
        return input_string.endswith(self.substring)


def contains(
    substrings: Union[str, List[str]],
    count: Optional[int] = None,
    error_message: Optional[str] = None,
    allow_empty: bool = True,
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

    return CountValidator(
        count_method=lambda a: sum(a.count(substring) for substring in substrings),
        count=count,
        expected_existence=expected_existence,
        expected_non_existence=expected_non_existence,
        expected_count=expected_count,
        allow_empty=allow_empty,
    )


def not_contains(
    substring: str, error_message: Optional[str] = None, allow_empty: bool = True
):
    return contains(
        substring, count=0, error_message=error_message, allow_empty=allow_empty
    )


class MatchRegex(BooleanValidator):

    def __init__(
        self,
        regex_string,
        error_message: Optional[str] = None,
        allow_empty: bool = True
    ):
        if error_message is None:
            error_message = "Input should match regex: {}".format(regex_string)
        super().__init__(error_message=error_message, allow_empty=allow_empty)
        self.regex_string = regex_string
    
    def is_valid(self, input_string: str):
        return bool(re.search(self.regex_string, input_string))


def contains_uppercase(
    count: Optional[int] = None,
    error_message: Optional[str] = None,
    allow_empty: bool = True,
):
    if error_message is not None:
        expected_non_existence = expected_count = expected_existence = error_message
    else:
        expected_existence = "Input should contain at least one uppercase character"
        expected_non_existence = "Input should not contain uppercase characters"
        expected_count = "Input should contain exactly {} uppercase characters".format(
            count
        )

    return CountValidator(
        count_method=lambda a: len([char for char in a if char in ascii_uppercase]),
        count=count,
        expected_existence=expected_existence,
        expected_non_existence=expected_non_existence,
        expected_count=expected_count,
        allow_empty=allow_empty,
    )


def contains_lowercase(
    count: Optional[int] = None,
    error_message: Optional[str] = None,
    allow_empty: bool = True,
):
    if error_message is not None:
        expected_non_existence = expected_count = expected_existence = error_message
    else:
        expected_existence = "Input should contain at least one lowercase character"
        expected_non_existence = "Input should not contain lowercase characters"
        expected_count = "Input should contain exactly {} lowercase characters".format(
            count
        )

    return CountValidator(
        count_method=lambda a: len([char for char in a if char in ascii_lowercase]),
        count=count,
        expected_existence=expected_existence,
        expected_non_existence=expected_non_existence,
        expected_count=expected_count,
        allow_empty=allow_empty,
    )


def contains_digit(
    count: Optional[int] = None,
    error_message: Optional[str] = None,
    allow_empty: bool = True,
):
    if error_message is not None:
        expected_non_existence = expected_count = expected_existence = error_message
    else:
        expected_existence = "Input should contain at least one digit"
        expected_non_existence = "Input should not contain digits"
        expected_count = "Input should contain exactly {} digits".format(count)

    return CountValidator(
        count_method=lambda a: len([char for char in a if char in digits]),
        count=count,
        expected_existence=expected_existence,
        expected_non_existence=expected_non_existence,
        expected_count=expected_count,
        allow_empty=allow_empty,
    )


def contains_special(
    count: Optional[int] = None,
    error_message: Optional[str] = None,
    allow_empty: bool = True,
):
    if error_message is not None:
        expected_non_existence = expected_count = expected_existence = error_message
    else:
        expected_existence = "Input should contain at least one special character"
        expected_non_existence = "Input should not contain specials characters"
        expected_count = "Input should contain exactly {} special characters".format(
            count
        )

    return CountValidator(
        count_method=lambda a: len(
            [char for char in a if not char.isalpha() and not char.isdigit()]
        ),
        count=count,
        expected_existence=expected_existence,
        expected_non_existence=expected_non_existence,
        expected_count=expected_count,
        allow_empty=allow_empty,
    )


class Integer(MatchRegex):

    INTEGER_REGEX = r"^[0-9]+$"

    def __init__(self, error_message: Optional[str] = None, allow_empty: bool = True):
        if error_message is None:
            error_message = "Input should be an integer"
        super().__init__(
            self.INTEGER_REGEX, error_message=error_message, allow_empty=allow_empty
        )


class Number(MatchRegex):

    NUMBER_REGEX = r"^[-]?(\d+|\d*\.\d+|\d+.\d*)$"

    def __init__(self, error_message: Optional[str] = None, allow_empty: bool = True):
        if error_message is None:
            error_message = "Input should be a number"
        super().__init__(
            self.NUMBER_REGEX, error_message=error_message, allow_empty=allow_empty
        )


class Email(MatchRegex):

    EMAIL_REGEX = (
        r"^[a-zA-Z][a-zA-Z0-9\.]*[a-zA-Z0-9]@[a-zA-Z][a-zA-Z0-9]*(\.[a-zA-Z0-9]+)+$"
    )

    def __init__(self, error_message: Optional[str] = None, allow_empty: bool = True):
        if error_message is None:
            error_message = "Input should be a valid email address"
        super().__init__(
            self.EMAIL_REGEX, error_message=error_message, allow_empty=allow_empty
        )


def combine(*validators):
    """Use this method to combine multiple validators."""

    def combined_validator(input_string):
        for validator in validators:
            error_message = validator(input_string)
            if error_message is not None:
                return error_message
        return None

    return combined_validator

