from toga.colors import rgba

# TODO: add non-ASCII strings.
TEXTS = ["", " ", "a", "ab", "abc", "hello world", "hello\nworld"]


# TODO: include None
components = [0, 1, 2, 128, 253, 254, 255]
alphas = [0.0, 0.01, 0.1, 0.5, 0.9, 0.99, 1.0]
COLORS = [
    rgba(r, g, b, a)
    for r in components
    for g in components
    for b in components
    for a in alphas
]
