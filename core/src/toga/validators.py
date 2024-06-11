from __future__ import annotations

import re
from abc import abstractmethod


class BooleanValidator:
    def __init__(self, error_message: str, allow_empty: bool = True):
        """An abstract base class for defining a simple validator.

        Subclasses should implement the ``is_valid()`` method

        :param error_message: The error to display to the user when the input
            isn't valid.
        :param allow_empty: Optional; Is no input considered valid? Defaults to
            ``True``
        """
        self.error_message = error_message
        self.allow_empty = allow_empty

    def __call__(self, input_string: str) -> str | None:
        if self.allow_empty and input_string == "":
            return None
        return None if self.is_valid(input_string) else self.error_message

    @abstractmethod
    def is_valid(self, input_string: str) -> bool:
        """Is the input string valid?

        :param input_string: The string to validate.
        :returns: ``True`` if the input is valid.
        """


class CountValidator:
    def __init__(
        self,
        count: int | None,
        expected_existence_message: str,
        expected_non_existence_message: str,
        expected_count_message: str,
        allow_empty: bool = True,
    ):
        """An abstract base class for validators that are based on counting
        instances of some content in the overall content.

        Subclasses should implement the ``count()`` method to identify the
        content of interest.

        :param count: Optional; The expected count.
        :param expected_existence_message: The error message to show if matches are
            expected, but were not found.
        :param expected_non_existence_message: The error message to show if matches were
            not expected, but were found.
        :param expected_count_message: The error message to show if matches
            were expected, but a different number were found.
        :param allow_empty: Optional; Is no input considered valid? Defaults to
            ``True``
        """
        self.expected_count = count
        self.expected_existence_message = expected_existence_message
        self.expected_non_existence_message = expected_non_existence_message
        self.expected_count_message = expected_count_message
        self.allow_empty = allow_empty

    def __call__(self, input_string: str) -> str | None:
        if self.allow_empty and input_string == "":
            return None
        actual_count = self.count(input_string)
        if actual_count == 0 and self.expected_count != 0:
            return self.expected_existence_message
        if actual_count != 0 and self.expected_count == 0:
            return self.expected_non_existence_message
        if self.expected_count is not None and actual_count != self.expected_count:
            return self.expected_count_message
        return None

    @abstractmethod
    def count(self, input_string: str) -> int:
        """Count the instances of content of interest in the input string.

        :param input_string: The string to inspect for content of interest.
        :returns: The number of instances of content that the validator is looking for.
        """


class LengthBetween(BooleanValidator):
    def __init__(
        self,
        min_length: int | None,
        max_length: int | None,
        error_message: str | None = None,
        allow_empty: bool = True,
    ):
        """A validator confirming that the length of input falls in a given
        range.

        :param min_length: The minimum length of the string (inclusive).
        :param max_length: The maximum length of the string (inclusive).
        :param error_message: Optional; the error message to display when the
            length isn't in the given range.
        :param allow_empty: Optional; Is no input considered valid? Defaults to
            ``True``
        """
        if error_message is None:
            error_message = (
                f"Input should be between {min_length} and {max_length} characters"
            )
        super().__init__(error_message=error_message, allow_empty=allow_empty)

        if (
            min_length is not None
            and max_length is not None
            and min_length > max_length
        ):
            raise ValueError("Minimum length cannot be less than maximum length")

        self.min_length = min_length
        self.max_length = max_length

    def is_valid(self, input_string: str) -> bool:
        if self.min_length is not None:
            if len(input_string) < self.min_length:
                return False
        if self.max_length is not None:
            if len(input_string) > self.max_length:
                return False
        return True


class MinLength(LengthBetween):
    def __init__(
        self,
        length: int,
        error_message: str | None = None,
        allow_empty: bool = True,
    ):
        """A validator confirming that the length of input exceeds a minimum size.

        :param length: The minimum length of the string (inclusive).
        :param error_message: Optional; the error message to display when the
            string isn't long enough.
        :param allow_empty: Optional; Is no input considered valid? Defaults to
            ``True``
        """
        if error_message is None:
            error_message = f"Input is too short (length should be at least {length})"
        super().__init__(
            min_length=length,
            max_length=None,
            error_message=error_message,
            allow_empty=allow_empty,
        )


class MaxLength(LengthBetween):
    def __init__(
        self,
        length: int,
        error_message: str | None = None,
    ):
        """A validator confirming that the length of input does not exceed a maximum size.

        :param length: The maximum length of the string (inclusive).
        :param error_message: Optional; the error message to display when the
            string is too long.
        """
        if error_message is None:
            error_message = f"Input is too long (length should be at most {length})"
        super().__init__(
            min_length=None,
            max_length=length,
            error_message=error_message,
        )


class StartsWith(BooleanValidator):
    def __init__(
        self,
        substring: str,
        error_message: str | None = None,
        allow_empty: bool = True,
    ):
        """A validator confirming that the input starts with a given substring.

        :param substring: The substring that the input must start with.
        :param error_message: Optional; the error message to display when the
            string doesn't start with the given substring.
        :param allow_empty: Optional; Is no input considered valid? Defaults to
            ``True``
        """
        if error_message is None:
            error_message = f"Input should start with {substring!r}"

        super().__init__(error_message=error_message, allow_empty=allow_empty)
        self.substring = substring

    def is_valid(self, input_string: str) -> bool:
        return input_string.startswith(self.substring)


class EndsWith(BooleanValidator):
    def __init__(
        self,
        substring: str,
        error_message: str | None = None,
        allow_empty: bool = True,
    ):
        """A validator confirming that the string ends with a given substring.

        :param substring: The substring that the input must end with.
        :param error_message: Optional; the error message to display when the
            string doesn't end with the given substring.
        :param allow_empty: Optional; Is no input considered valid? Defaults to
            ``True``
        """
        if error_message is None:
            error_message = f"Input should end with '{substring}'"

        super().__init__(error_message=error_message, allow_empty=allow_empty)
        self.substring = substring

    def is_valid(self, input_string: str) -> bool:
        return input_string.endswith(self.substring)


class Contains(CountValidator):
    def __init__(
        self,
        substring: str,
        count: int | None = None,
        error_message: str | None = None,
        allow_empty: bool = True,
    ):
        """A validator confirming that the string contains one or more
        copies of a substring.

        :param substring: The substring that must exist in the input.
        :param count: Optional; The exact number of matches that are expected.
        :param error_message: Optional; the error message to display when the
            input doesn't contain the substring (or the requested count of substrings).
        :param allow_empty: Optional; Is no input considered valid? Defaults to
            ``True``
        """
        if error_message is not None:
            expected_non_existence_message = error_message
            expected_count_message = error_message
            expected_existence_message = error_message
        else:
            expected_existence_message = f"Input should contain {substring!r}"
            expected_non_existence_message = f"Input should not contain {substring!r}"
            expected_count_message = (
                f"Input should contain {substring!r} exactly {count} times"
            )

        super().__init__(
            count=count,
            expected_existence_message=expected_existence_message,
            expected_non_existence_message=expected_non_existence_message,
            expected_count_message=expected_count_message,
            allow_empty=allow_empty,
        )
        self.substring = substring

    def count(self, input_string: str) -> int:
        return input_string.count(self.substring)


class NotContains(Contains):
    def __init__(
        self,
        substring: str,
        error_message: str | None = None,
    ):
        """A validator confirming that the string does not contain a substring.

        :param substring: A substring that must not exist in the input.
        :param error_message: Optional; the error message to display when the
            input contains the provided substring.
        """
        super().__init__(
            substring,
            count=0,
            error_message=error_message,
        )


class MatchRegex(BooleanValidator):
    def __init__(
        self,
        regex_string: str,
        error_message: str | None = None,
        allow_empty: bool = True,
    ):
        """A validator confirming that the string matches a given regular expression.

        :param regex_string: A regular expression that the input must match.
        :param error_message: Optional; the error message to display when the
            input doesn't match the provided regular expression.
        :param allow_empty: Optional; Is no input considered valid? Defaults to
            ``True``
        """
        if error_message is None:
            error_message = f"Input should match regex: {regex_string!r}"

        super().__init__(error_message=error_message, allow_empty=allow_empty)
        self.regex_string = regex_string

    def is_valid(self, input_string: str) -> bool:
        return bool(re.search(self.regex_string, input_string))


class ContainsUppercase(CountValidator):
    def __init__(
        self,
        count: int | None = None,
        error_message: str | None = None,
        allow_empty: bool = True,
    ):
        """A validator confirming that the string contains upper case letters.

        :param count: Optional; if provided, the exact count of upper
            case letters that must exist. If not provided, the existence of any
            upper case letter will make the string valid.
        :param error_message: Optional; the error message to display when the
            input doesn't contain upper case letters (or the requested count of
            upper case letters).
        :param allow_empty: Optional; Is no input considered valid? Defaults to
            ``True``
        """
        if error_message is not None:
            expected_non_existence_message = error_message
            expected_count_message = error_message
            expected_existence_message = error_message
        else:
            expected_existence_message = (
                "Input should contain at least one upper case character"
            )
            expected_non_existence_message = (
                "Input should not contain upper case characters"
            )
            expected_count_message = (
                f"Input should contain exactly {count} upper case characters"
            )

        super().__init__(
            count=count,
            expected_existence_message=expected_existence_message,
            expected_non_existence_message=expected_non_existence_message,
            expected_count_message=expected_count_message,
            allow_empty=allow_empty,
        )

    def count(self, input_string: str) -> int:
        return len([char for char in input_string if char.isupper()])


class ContainsLowercase(CountValidator):
    def __init__(
        self,
        count: int | None = None,
        error_message: str | None = None,
        allow_empty: bool = True,
    ):
        """A validator confirming that the string contains lower case letters.

        :param count: Optional; if provided, the exact count of lower
            case letters that must exist. If not provided, the existence of any
            lower case letter will make the string valid.
        :param error_message: Optional; the error message to display when the
            input doesn't contain lower case letters (or the requested count of
            lower case letters).
        :param allow_empty: Optional; Is no input considered valid? Defaults to
            ``True``
        """
        if error_message is not None:
            expected_non_existence_message = error_message
            expected_count_message = error_message
            expected_existence_message = error_message
        else:
            expected_existence_message = (
                "Input should contain at least one lower case character"
            )
            expected_non_existence_message = (
                "Input should not contain lower case characters"
            )
            expected_count_message = (
                f"Input should contain exactly {count} lower case characters"
            )

        super().__init__(
            count=count,
            expected_existence_message=expected_existence_message,
            expected_non_existence_message=expected_non_existence_message,
            expected_count_message=expected_count_message,
            allow_empty=allow_empty,
        )

    def count(self, input_string: str) -> int:
        return len([char for char in input_string if char.islower()])


class ContainsDigit(CountValidator):
    def __init__(
        self,
        count: int | None = None,
        error_message: str | None = None,
        allow_empty: bool = True,
    ):
        """A validator confirming that the string contains digits.

        :param count: Optional; if provided, the exact count of digits
            that must exist. If not provided, the existence of any digit will
            make the string valid.
        :param error_message: Optional; the error message to display when the
            input doesn't contain digits (or the requested count of digits).
        :param allow_empty: Optional; Is no input considered valid? Defaults to
            ``True``
        """
        if error_message is not None:
            expected_non_existence_message = error_message
            expected_count_message = error_message
            expected_existence_message = error_message
        else:
            expected_existence_message = "Input should contain at least one digit"
            expected_non_existence_message = "Input should not contain digits"
            expected_count_message = f"Input should contain exactly {count} digits"

        super().__init__(
            count=count,
            expected_existence_message=expected_existence_message,
            expected_non_existence_message=expected_non_existence_message,
            expected_count_message=expected_count_message,
            allow_empty=allow_empty,
        )

    def count(self, input_string: str) -> int:
        return len([char for char in input_string if char.isdigit()])


class ContainsSpecial(CountValidator):
    def __init__(
        self,
        count: int | None = None,
        error_message: str | None = None,
        allow_empty: bool = True,
    ):
        """A validator confirming that the string contains "special" (i.e.,
        non-alphanumeric) characters.

        :param count: Optional; if provided, the exact count of special
            characters that must exist. If not provided, the existence of any
            special character will make the string valid.
        :param error_message: Optional; the error message to display when the
            input doesn't contain special characters (or the requested count of
            special characters).
        :param allow_empty: Optional; Is no input considered valid? Defaults to
            ``True``
        """
        if error_message is not None:
            expected_non_existence_message = error_message
            expected_count_message = error_message
            expected_existence_message = error_message
        else:
            expected_existence_message = (
                "Input should contain at least one special character"
            )
            expected_non_existence_message = (
                "Input should not contain special characters"
            )
            expected_count_message = (
                f"Input should contain exactly {count} special characters"
            )

        super().__init__(
            count=count,
            expected_existence_message=expected_existence_message,
            expected_non_existence_message=expected_non_existence_message,
            expected_count_message=expected_count_message,
            allow_empty=allow_empty,
        )

    def count(self, input_string: str) -> int:
        return len(
            [
                char
                for char in input_string
                if not char.isalpha() and not char.isdigit() and not char.isspace()
            ]
        )


class Integer(BooleanValidator):
    def __init__(
        self,
        error_message: str | None = None,
        allow_empty: bool = True,
    ):
        """A validator confirming that the string is an integer.

        :param error_message: Optional; the error message to display when the
            input isn't an integer.
        :param allow_empty: Optional; Is no input considered valid? Defaults to
            ``True``
        """
        if error_message is None:
            error_message = "Input should be an integer"
        super().__init__(error_message=error_message, allow_empty=allow_empty)

    def is_valid(self, input_string: str) -> bool:
        try:
            int(input_string)
            return True
        except ValueError:
            return False


class Number(BooleanValidator):
    def __init__(
        self,
        error_message: str | None = None,
        allow_empty: bool = True,
    ):
        """A validator confirming that the string is a number.

        :param error_message: Optional; the error message to display when the
            input isn't a number.
        :param allow_empty: Optional; Is no input considered valid? Defaults to
            ``True``
        """
        if error_message is None:
            error_message = "Input should be a number"
        super().__init__(error_message=error_message, allow_empty=allow_empty)

    def is_valid(self, input_string: str) -> bool:
        try:
            float(input_string)
            return True
        except ValueError:
            return False


class Email(MatchRegex):
    EMAIL_REGEX = (
        r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
    )

    def __init__(
        self,
        error_message: str | None = None,
        allow_empty: bool = True,
    ):
        """A validator confirming that the string is an email address.

        .. note::

            It's impossible to do *true* RFC-compliant email validation with a regex.
            This validator does a "best effort" validation. It will inevitably allow
            some email addresses that aren't *technically* valid. However, it shouldn't
            *exclude* any valid email addresses.

        :param error_message: Optional; the error message to display when the
            input isn't a number.
        :param allow_empty: Optional; Is no input considered valid? Defaults to
            ``True``
        """
        if error_message is None:
            error_message = "Input should be a valid email address"
        super().__init__(
            self.EMAIL_REGEX, error_message=error_message, allow_empty=allow_empty
        )
