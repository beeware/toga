from toga import validators
import unittest


class TestValidators(unittest.TestCase):
    def setUp(self):
        self.args = []
        self.kwargs = {}
        self.validator_factory = None
        self.valid_inputs = []
        self.invalid_inputs = []
        self.check_empty = True

    def check(self):
        if self.validator_factory is None:
            self.fail("Validator is not set!")
        self.check_validator(
            self.validator_factory(*self.args, **self.kwargs),
            valid_inputs=self.valid_inputs,
            invalid_inputs=self.invalid_inputs,
        )
        dummy_error = "This is a dummy error message!"
        self.check_validator(
            self.validator_factory(
                *self.args, **self.kwargs, error_message=dummy_error
            ),
            valid_inputs=self.valid_inputs,
            invalid_inputs=[
                (input_string, dummy_error)
                for input_string, error_message in self.invalid_inputs
            ],
        )
        if self.check_empty:
            self.assertIsNone(
                self.validator_factory(
                    *self.args, **self.kwargs, error_message=dummy_error, allow_empty=True
                )("")
            )
            self.assertEqual(
                self.validator_factory(
                    *self.args, **self.kwargs, error_message=dummy_error, allow_empty=False
                )(""),
                dummy_error
            )

    def check_validator(self, validator, valid_inputs, invalid_inputs):
        for valid_input in valid_inputs:
            self.assertIsNone(
                validator(valid_input),
                msg='"{}" should be a valid input, but it is not'.format(valid_input),
            )
        for invalid_input, error_message in invalid_inputs:
            self.assertEqual(
                error_message,
                validator(invalid_input),
                msg='"{}" error message is different than expected.'.format(
                    invalid_input
                ),
            )

    def test_validate_minimum_length(self):
        default_error_message = "Input is too short (length should be at least 5)"

        self.args = [5]
        self.validator_factory = validators.MinLength
        self.valid_inputs = ["I am long enough", "right", "longer"]
        self.invalid_inputs = [
            ("I", default_error_message),
            ("am", default_error_message),
            ("tiny", default_error_message),
        ]

        self.check()

    def test_validate_maximum_length(self):
        default_error_message = "Input is too long (length should be at most 10)"

        self.args = [10]
        self.validator_factory = validators.MaxLength
        self.valid_inputs = ["", "I am good", "nice", "a"]
        self.invalid_inputs = [
            ("I am way too long", default_error_message),
            ("are you serious now?", default_error_message),
        ]
        self.check_empty = False

        self.check()

    def test_validate_length_between(self):
        default_error_message = "Input should be between 5 and 10 characters"

        self.args = [5, 10]
        self.validator_factory = validators.LengthBetween
        self.valid_inputs = ["I am good", "right", "123456789"]
        self.invalid_inputs = [
            ("I", default_error_message),
            ("am", default_error_message),
            ("tiny", default_error_message),
            ("I am way too long", default_error_message),
            ("are you serious now?", default_error_message),
        ]

        self.check()

    def test_validate_startswith(self):
        default_error_message = 'Input should start with "good"'

        self.args = ["good"]
        self.validator_factory = validators.StartsWith
        self.valid_inputs = [
            "good to be back", "goodness!", "goody", "good, good, good"
        ]
        self.invalid_inputs = [
            ("no good", default_error_message),
            ("I am so bad", default_error_message),
            ("goo goo dolls", default_error_message),
            ("go od", default_error_message),
            (
                "It doesn't matter if I'm good, if I don't start with it",
                default_error_message
            ),
        ]

        self.check()

    def test_validate_endswith(self):
        default_error_message = 'Input should end with "good"'

        self.args = ["good"]
        self.validator_factory = validators.EndsWith
        self.valid_inputs = [
            "go back to good", "It is so good", "good", "good, good, good"
        ]
        self.invalid_inputs = [
            ("good start, but no", default_error_message),
            ("I am so bad", default_error_message),
            ("goo goo dolls", default_error_message),
            ("go od", default_error_message),
            (
                "It doesn't matter if I'm good, if I don't end with it",
                default_error_message
            ),
        ]

        self.check()

    def test_validate_contains(self):
        default_error_message = 'Input should contain "good"'

        self.args = ["good"]
        self.validator_factory = validators.Contains
        self.valid_inputs = ["This is very good", "goodness", "goody", "nogood"]
        self.invalid_inputs = [
            ("I am so bad", default_error_message),
            ("goo goo dolls", default_error_message),
            ("go od", default_error_message),
        ]

        self.check()

    def test_validate_contains_once(self):
        self.args = ["good"]
        self.kwargs = dict(compare_count=1)
        self.validator_factory = validators.Contains
        self.valid_inputs = ["This is very good", "goodness", "goody", "nogood"]
        self.invalid_inputs = [
            ("I am so bad", 'Input should contain "good"'),
            ("good, very good", 'Input should contain "good" exactly 1 times'),
            (
                "it's good to be so good in being good",
                'Input should contain "good" exactly 1 times'
            ),
        ]

        self.check()

    def test_validate_contains_zero_times(self):
        self.args = ["bad"]
        self.kwargs = dict(compare_count=0)
        self.validator_factory = validators.Contains
        self.valid_inputs = [
            "", "This is very good", "goodness", "goody", "nogood", "good, very good"
        ]
        self.invalid_inputs = [
            ("I am so bad", 'Input should not contain "bad"'),
            ("Why being so baddy?", 'Input should not contain "bad"'),
            ("sinbad", 'Input should not contain "bad"'),
        ]
        self.check_empty = False

        self.check()

    def test_validate_not_contains(self):
        self.args = ["bad"]
        self.validator_factory = validators.NotContains
        self.valid_inputs = [
            "", "This is very good", "goodness", "goody", "nogood", "good, very good"
        ]
        self.invalid_inputs = [
            ("I am so bad", 'Input should not contain "bad"'),
            ("Why being so baddy?", 'Input should not contain "bad"'),
            ("sinbad", 'Input should not contain "bad"'),
        ]
        self.check_empty = False

        self.check()

    def test_validate_contains_two_words(self):
        default_error_message = 'Input should contain "good" or "bad"'

        self.args = [["good", "bad"]]
        self.validator_factory = validators.Contains
        self.valid_inputs = [
            "There are always good and bad in life",
            "bad before good",
            "good, good, bad",
            "I am so bad",
            "I am so good",
        ]
        self.invalid_inputs = [
            ("wanted words are not here", default_error_message),
            ("go od", default_error_message),
            ("b ad", default_error_message),
        ]

        self.check()

    def test_validate_match_regex(self):
        default_error_message = "Input should match regex: [A-Z]{1}[a-z]{2}[A-Z]{1}"

        self.args = ["[A-Z]{1}[a-z]{2}[A-Z]{1}"]
        self.validator_factory = validators.MatchRegex
        self.valid_inputs = [
            "GooD", "partial is AlsO good in this case"
        ]
        self.invalid_inputs = [
            ("Good", default_error_message),
            ("gooD", default_error_message),
            ("Goo", default_error_message),
            ("Goo2", default_error_message),
            ("!Goo", default_error_message),
        ]

        self.check()

    def test_contains_uppercase(self):
        self.validator_factory = validators.ContainsUppercase
        self.valid_inputs = [
            "Good", "using Toga is very helpful", "ending with uppercase workS"
        ]
        self.invalid_inputs = [
            (
                "lowercase is not helpful",
                "Input should contain at least one uppercase character"
            ),
        ]

        self.check()

    def test_contains_two_uppercase(self):
        self.kwargs = dict(compare_count=2)
        self.validator_factory = validators.ContainsUppercase
        self.valid_inputs = [
            "GooD", "using TogA is very helpful"
        ]
        self.invalid_inputs = [
            (
                "no uppercase is no good",
                "Input should contain at least one uppercase character"
            ),
            (
                "One uppercase is not enough",
                "Input should contain exactly 2 uppercase characters"
            ),
            (
                "Three Is a Crowd",
                "Input should contain exactly 2 uppercase characters"
            ),
        ]

        self.check()

    def test_contains_lowercase(self):
        self.validator_factory = validators.ContainsLowercase
        self.valid_inputs = [
            "gOOD", "USING tOGA IS VERY HELPFUL", "ENDING WITH LOWERCASE WORKs"
        ]
        self.invalid_inputs = [
            (
                "STOP YELLING!",
                "Input should contain at least one lowercase character"
            ),
        ]

        self.check()

    def test_contains_two_lowercase(self):
        self.kwargs = dict(compare_count=2)
        self.validator_factory = validators.ContainsLowercase
        self.valid_inputs = [
            "GooD", "USING tOGa IS VERY HELPFUL"
        ]
        self.invalid_inputs = [
            (
                "NO LOWERCASE IS NO GOOD",
                "Input should contain at least one lowercase character"
            ),
            (
                "oNE LOWERCASE IS NOT ENOUGH",
                "Input should contain exactly 2 lowercase characters"
            ),
            (
                "tHREE iS A cROWD",
                "Input should contain exactly 2 lowercase characters"
            ),
        ]

        self.check()

    def test_contains_digit(self):
        self.validator_factory = validators.ContainsDigit
        self.valid_inputs = [
            "1) start counting", "count 2 and continue", "ends with 3"
        ]
        self.invalid_inputs = [
            ("no digits in here", "Input should contain at least one digit"),
        ]

        self.check()

    def test_contains_two_digits(self):
        self.kwargs = dict(compare_count=2)
        self.validator_factory = validators.ContainsDigit
        self.valid_inputs = [
            "1+2", "the number 3 is bigger than 1",
        ]
        self.invalid_inputs = [
            ("no digits in here", "Input should contain at least one digit"),
            ("only 1 digit is not enough", "Input should contain exactly 2 digits"),
            ("3 is w4y 2 much", "Input should contain exactly 2 digits"),
        ]

        self.check()

    def test_contains_special(self):
        default_error_message = "Input should contain at least one special character"

        self.validator_factory = validators.ContainsSpecial
        self.valid_inputs = ["Hey!", "tiberius@beeware.org", "#1"]
        self.invalid_inputs = [
            ("bad", default_error_message),
            ("123", default_error_message)
        ]

        self.check()

    def test_contains_two_special(self):
        self.kwargs = dict(compare_count=2)
        self.validator_factory = validators.ContainsSpecial
        self.valid_inputs = ["!Hey!", "tiberius@beeware.org", "#1#"]
        self.invalid_inputs = [
            ("nospecial", "Input should contain at least one special character"),
            ("notenough!", "Input should contain exactly 2 special characters"),
            ("this is too much", "Input should contain exactly 2 special characters"),
        ]

        self.check()

    def test_integer(self):
        default_error_message = "Input should be an integer"

        self.validator_factory = validators.Integer
        self.valid_inputs = ["0", "00", "1", "21", "1234", "12423571"]
        self.invalid_inputs = [
            ("a", default_error_message),
            ("ab", default_error_message),
            ("this is a not valid!", default_error_message),
            ("0.0", default_error_message),
            ("2.1", default_error_message),
            ("-0.22", default_error_message),
            (".2", default_error_message),
            ("88.0", default_error_message),
            ("9.", default_error_message)
        ]

        self.check()

    def test_number(self):
        default_error_message = "Input should be a number"

        self.validator_factory = validators.Number
        self.valid_inputs = [
            "0",
            "00",
            "0.0",
            "1",
            "2.1",
            "-1",
            "-0.22",
            ".2",
            "88.0",
            "9.",
            "2e+7",
            "9e-6",
            "1.23e+15",
            "-9.2E+23",
            "1.23e-15",
            "-9.2E-23",
        ]
        self.invalid_inputs = [
            ("a", default_error_message),
            ("ab", default_error_message),
            ("this is a not valid!", default_error_message),
            (".", default_error_message),
            ("88.a", default_error_message),
            ("e+12", default_error_message),
            ("E-9", default_error_message),
        ]

        self.check()

    def test_email(self):
        default_error_message = "Input should be a valid email address"

        self.validator_factory = validators.Email
        self.valid_inputs = [
            "tiberius@beeware.org",
            "tiberius.yak@beeware.org",
            "tiberius@beeware.ab.cd"
        ]
        self.invalid_inputs = [
            ("2iberius@beeware.org", default_error_message),
            ("tiberius.beeware.org", default_error_message),
            ("tiberius@me@beeware.org", default_error_message),
            ("tiberius@beeware", default_error_message),
            ("tiberius@beeware.", default_error_message)
        ]

        self.check()
