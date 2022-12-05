from toga.colors import rgba

# TODO: add non-ASCII strings.
TEXTS = ["", " ", "a", "ab", "abc", "hello world", "hello\nworld"]


# TODO: include None
COLORS = [
    rgba(r, g, b, a)
    for r, g, b in [
        # Black, gray, white,
        (0, 0, 0),
        (1, 1, 1),
        (10, 10, 10),
        (128, 128, 128),
        (245, 245, 245),
        (254, 254, 254),
        (255, 255, 255),
        # Primaries
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
    ]
    for a in [0.0, 0.01, 0.1, 0.5, 0.9, 0.99, 1.0]
]
