import re
from string import ascii_lowercase, ascii_uppercase, digits
from typing import List, Optional, Union


class BooleanValidator:
    def __init__(self, error_message: str, allow_empty: bool = True):
        self.error_message = error_message
        self.allow_empty = allow_empty

    def __call__(self, input_string: str):
        if self.allow_empty and input_string == "":
            return None
        return None if self.is_valid(input_string) else self.error_message

    def is_valid(self, input_string: str):
        raise NotImplementedError(
            "is_valid is not implemented in BooleanValidator. " "Please override it."
        )


class CountValidator:
    def __init__(
        self,
        compare_count: Optional[int],
        expected_existence: str,
        expected_non_existence: str,
        expected_count: str,
        allow_empty: bool = True,
    ):
        self.compare_count = compare_count
        self.expected_existence = expected_existence
        self.expected_non_existence = expected_non_existence
        self.expected_count = expected_count
        self.allow_empty = allow_empty

    def __call__(self, input_string: str):
        if self.allow_empty and input_string == "":
            return None
        actual_count = self.count(input_string)
        if actual_count == 0 and self.compare_count != 0:
            return self.expected_existence
        if actual_count != 0 and self.compare_count == 0:
            return self.expected_non_existence
        if self.compare_count is not None and actual_count != self.compare_count:
            return self.expected_count
        return None

    def count(self, input_string: str):
        raise NotImplementedError(
            "count is not implemented in CountValidator. " "Please override it."
        )


class LengthBetween(BooleanValidator):
    def __init__(
        self,
        min_value: int,
        max_value: int,
        error_message: Optional[str] = None,
        allow_empty: bool = True,
    ):
        if error_message is None:
            error_message = "Input should be between {} and {} characters".format(
                min_value, max_value
            )
        super().__init__(error_message=error_message, allow_empty=allow_empty)
        self.min_value = min_value
        self.max_value = max_value

    def is_valid(self, input_string: str):
        if self.min_value:
            if len(input_string) < self.min_value:
                return False
        if self.max_value:
            if len(input_string) > self.max_value:
                return False
        return True


class MinLength(LengthBetween):
    def __init__(
        self, length: int, error_message: Optional[str] = None, allow_empty: bool = True
    ):
        if error_message is None:
            error_message = "Input is too short (length should be at least {})".format(
                length
            )
        super().__init__(
            min_value=length,
            max_value=None,
            error_message=error_message,
            allow_empty=allow_empty,
        )


class MaxLength(LengthBetween):
    def __init__(
        self, length: int, error_message: Optional[str] = None, allow_empty: bool = True
    ):
        if error_message is None:
            error_message = "Input is too long (length should be at most {})".format(
                length
            )
        super().__init__(
            min_value=None,
            max_value=length,
            error_message=error_message,
            allow_empty=allow_empty,
        )


class StartsWith(BooleanValidator):
    def __init__(
        self,
        substring: str,
        error_message: Optional[str] = None,
        allow_empty: bool = True,
    ):
        if error_message is None:
            error_message = f'Input should start with "{substring}"'

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
            error_message = f'Input should end with "{substring}"'

        super().__init__(error_message=error_message, allow_empty=allow_empty)
        self.substring = substring

    def is_valid(self, input_string: str):
        return input_string.endswith(self.substring)


class Contains(CountValidator):
    def __init__(
        self,
        substrings: Union[str, List[str]],
        compare_count: Optional[int] = None,
        error_message: Optional[str] = None,
        allow_empty: bool = True,
    ):
        if isinstance(substrings, str):
            substrings = [substrings]

        if error_message is not None:
            expected_non_existence = expected_count = expected_existence = error_message
        else:
            if len(substrings) == 1:
                substrings_string = f'"{substrings[0]}"'
            else:
                substrings_string = (
                    ", ".join(f'"{substring}"' for substring in substrings[:-1])
                    + f' or "{substrings[-1]}"'
                )
            expected_existence = f"Input should contain {substrings_string}"
            expected_non_existence = "Input should not contain {}".format(
                substrings_string
            )
            expected_count = "Input should contain {} exactly {} times".format(
                substrings_string, compare_count
            )

        super().__init__(
            compare_count=compare_count,
            expected_existence=expected_existence,
            expected_non_existence=expected_non_existence,
            expected_count=expected_count,
            allow_empty=allow_empty,
        )
        self.substrings = substrings

    def count(self, input_string: str):
        return sum(input_string.count(substring) for substring in self.substrings)


class NotContains(Contains):
    def __init__(
        self,
        substring: str,
        error_message: Optional[str] = None,
        allow_empty: bool = True,
    ):
        super().__init__(
            substring,
            compare_count=0,
            error_message=error_message,
            allow_empty=allow_empty,
        )


class MatchRegex(BooleanValidator):
    def __init__(
        self,
        regex_string,
        error_message: Optional[str] = None,
        allow_empty: bool = True,
    ):
        if error_message is None:
            error_message = f"Input should match regex: {regex_string}"
        super().__init__(error_message=error_message, allow_empty=allow_empty)
        self.regex_string = regex_string

    def is_valid(self, input_string: str):
        return bool(re.search(self.regex_string, input_string))


class ContainsUppercase(CountValidator):
    def __init__(
        self,
        compare_count: Optional[int] = None,
        error_message: Optional[str] = None,
        allow_empty: bool = True,
    ):
        if error_message is not None:
            expected_non_existence = expected_count = expected_existence = error_message
        else:
            expected_existence = "Input should contain at least one uppercase character"
            expected_non_existence = "Input should not contain uppercase characters"
            expected_count = (
                "Input should contain exactly {} uppercase characters".format(
                    compare_count
                )
            )

        super().__init__(
            compare_count=compare_count,
            expected_existence=expected_existence,
            expected_non_existence=expected_non_existence,
            expected_count=expected_count,
            allow_empty=allow_empty,
        )

    def count(self, input_string: str):
        return len([char for char in input_string if char in ascii_uppercase])


class ContainsLowercase(CountValidator):
    def __init__(
        self,
        compare_count: Optional[int] = None,
        error_message: Optional[str] = None,
        allow_empty: bool = True,
    ):
        if error_message is not None:
            expected_non_existence = expected_count = expected_existence = error_message
        else:
            expected_existence = "Input should contain at least one lowercase character"
            expected_non_existence = "Input should not contain lowercase characters"
            expected_count = (
                "Input should contain exactly {} lowercase characters".format(
                    compare_count
                )
            )

        super().__init__(
            compare_count=compare_count,
            expected_existence=expected_existence,
            expected_non_existence=expected_non_existence,
            expected_count=expected_count,
            allow_empty=allow_empty,
        )

    def count(self, input_string: str):
        return len([char for char in input_string if char in ascii_lowercase])


class ContainsDigit(CountValidator):
    def __init__(
        self,
        compare_count: Optional[int] = None,
        error_message: Optional[str] = None,
        allow_empty: bool = True,
    ):
        if error_message is not None:
            expected_non_existence = expected_count = expected_existence = error_message
        else:
            expected_existence = "Input should contain at least one digit"
            expected_non_existence = "Input should not contain digits"
            expected_count = "Input should contain exactly {} digits".format(
                compare_count
            )

        super().__init__(
            compare_count=compare_count,
            expected_existence=expected_existence,
            expected_non_existence=expected_non_existence,
            expected_count=expected_count,
            allow_empty=allow_empty,
        )

    def count(self, input_string: str):
        return len([char for char in input_string if char in digits])


class ContainsSpecial(CountValidator):
    def __init__(
        self,
        compare_count: Optional[int] = None,
        error_message: Optional[str] = None,
        allow_empty: bool = True,
    ):
        if error_message is not None:
            expected_non_existence = expected_count = expected_existence = error_message
        else:
            expected_existence = "Input should contain at least one special character"
            expected_non_existence = "Input should not contain specials characters"
            expected_count = (
                "Input should contain exactly {} special characters".format(
                    compare_count
                )
            )

        super().__init__(
            compare_count=compare_count,
            expected_existence=expected_existence,
            expected_non_existence=expected_non_existence,
            expected_count=expected_count,
            allow_empty=allow_empty,
        )

    def count(self, input_string: str):
        return len(
            [char for char in input_string if not char.isalpha() and not char.isdigit()]
        )


class Integer(MatchRegex):
    INTEGER_REGEX = r"^\d+$"

    def __init__(self, error_message: Optional[str] = None, allow_empty: bool = True):
        if error_message is None:
            error_message = "Input should be an integer"
        super().__init__(
            self.INTEGER_REGEX, error_message=error_message, allow_empty=allow_empty
        )


class Number(MatchRegex):
    NUMBER_REGEX = r"^[-+]?(\d+\.|\d*\.?\d+)([eE][-+]?\d+)?$"

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
