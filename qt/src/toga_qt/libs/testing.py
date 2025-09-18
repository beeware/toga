import os


class AnyWithin:
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def __eq__(self, other):
        if isinstance(other, AnyWithin):
            return max(self.low, other.low) <= min(self.high, other.high)
        try:
            return self.low <= other <= self.high
        except TypeError:
            return False

    def __lt__(self, other):
        if isinstance(other, AnyWithin):
            return self.high < other.low
        return self.high < other

    def __le__(self, other):
        if isinstance(other, AnyWithin):
            return self.high <= other.low
        return self.high <= other

    def __gt__(self, other):
        if isinstance(other, AnyWithin):
            return self.low > other.high
        return self.low > other

    def __ge__(self, other):
        if isinstance(other, AnyWithin):
            return self.low >= other.high
        return self.low >= other

    def __add__(self, other):
        if isinstance(other, AnyWithin):
            return AnyWithin(self.low + other.low, self.high + other.high)
        elif isinstance(other, (int, float)):
            return AnyWithin(self.low + other, self.high + other)
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, AnyWithin):
            return AnyWithin(self.low - other.high, self.high - other.low)
        elif isinstance(other, (int, float)):
            return AnyWithin(self.low - other, self.high - other)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, AnyWithin):
            return AnyWithin(other.low - self.high, other.high - self.low)
        elif isinstance(other, (int, float)):
            return AnyWithin(other - self.high, other - self.low)
        return NotImplemented

    def __repr__(self):
        return f"AnyWithin({self.low}, {self.high})"


def get_testing():
    return bool(os.environ.get("PYTEST_VERSION"))
