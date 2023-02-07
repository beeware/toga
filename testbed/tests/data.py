from toga.colors import rgba

TEXTS = ["", " ", "a", "ab", "abc", "hello world", "hello\nworld", "你好, wørłd!"]


COLORS = [
    # Avoid using (0, 0, 0, 0.0) as a test color,
    # as that is indistinguishable from the TRANSPARENT color
    rgba(r, g, b, a)
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
