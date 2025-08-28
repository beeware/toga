# A test object that can be used as data
class MyObject:
    def __str__(self):
        return "My Test Object"


# The text examples must both increase and decrease in size between examples to
# ensure that reducing the size of a label doesn't prevent future labels from
# increasing in size.
TEXTS = [
    "example",
    "",
    "a",
    " ",
    "ab",
    "abc",
    "hello world",
    "hello\nworld",
    "你好, wørłd!",
    1234,
    MyObject(),
]