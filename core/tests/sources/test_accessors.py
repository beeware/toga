import pytest

from toga.sources.accessors import build_accessors, to_accessor


@pytest.mark.parametrize(
    "heading, accessor",
    [
        ("hello", "hello"),
        ("hello", "hello"),
        ("Hello", "hello"),
        ("Hello1", "hello1"),
        ("Hello 1", "hello_1"),
        ("1 Hello", "_1_hello"),
        ("Hello world", "hello_world"),
        ("Hello World", "hello_world"),
        ("Hello World 1", "hello_world_1"),
        ("Hello World 1!", "hello_world_1"),
        ("1 Hello World", "_1_hello_world"),
        ("1 Hello World!", "_1_hello_world"),
        ("Hello!$@# World!^&*(", "hello_world"),
        (" ", "_"),
        # Multiple whitespace characters are collapsed
        ("Hello - World", "hello_world"),
        ("  ", "_"),
    ],
)
def test_to_accessor(heading, accessor):
    """Headings can be converted into accessors."""

    assert to_accessor(heading) == accessor


@pytest.mark.parametrize("heading", ["$*(!&*@&^*&^!", ""])
def test_to_accessor_failures(heading):
    with pytest.raises(
        ValueError,
        match=r"Unable to automatically generate accessor from heading '.*'",
    ):
        to_accessor(heading)


@pytest.mark.parametrize(
    "headings, overrides, accessors",
    [
        # No overrides
        (
            ["First Col", "Second Col", "Third Col"],
            None,
            ["first_col", "second_col", "third_col"],
        ),
        # Explicitly provided accessors
        (
            ["First Col", "Second Col", "Third Col"],
            ["first", "second", "third"],
            ["first", "second", "third"],
        ),
        # Override some accessors
        (
            ["First Col", "Second Col", "Third Col"],
            ["first", "second", None],
            ["first", "second", "third_col"],
        ),
        # Override some accessors using dictionary
        (
            ["First Col", "Second Col", "Third Col"],
            {"First Col": "first", "Second Col": "second"},
            ["first", "second", "third_col"],
        ),
    ],
)
def test_build_accessors(headings, overrides, accessors):
    """Accessors can be constructed from headings with overrides."""
    assert build_accessors(headings, overrides) == accessors


@pytest.mark.parametrize(
    "headings, overrides, error",
    [
        (
            ["First Col", "Second Col", "Third Col"],
            ["first", "second"],
            r"Number of accessors must match number of headings",
        ),
        (
            ["!!", "Second Col", "Third Col"],
            None,
            r"Unable to automatically generate accessor from heading '!!'",
        ),
    ],
)
def test_build_accessor_failure(headings, overrides, error):
    """If an accessor list can't be built, an error is raised."""
    with pytest.raises(ValueError, match=error):
        build_accessors(headings, overrides)
