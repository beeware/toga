from toga.colors import rgb


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


COLORS = [
    # Avoid using (0, 0, 0, 0.0) as a test color,
    # as that is indistinguishable from the TRANSPARENT color
    rgb(r, g, b, a)
    for r, g, b, a in [
        # Black, gray, white,
        (0, 0, 0, 1.0),
        (128, 128, 128, 1.0),
        (255, 255, 255, 1.0),
        # Primaries
        (255, 0, 0, 1.0),
        (0, 255, 0, 1.0),
        (0, 0, 255, 1.0),
        # Color with different channel values, including transparency
        (50, 128, 200, 0.0),
        (50, 128, 200, 0.5),
        (50, 128, 200, 0.9),
        (50, 128, 200, 1.0),
    ]
]
