from __future__ import annotations

import re

NON_ACCESSOR_CHARS = re.compile(r"[^\w ]")
WHITESPACE = re.compile(r"\s+")


def to_accessor(heading: str) -> str:
    """Convert a human-readable heading into a data attribute accessor.

    This is done by:

    1. Converting the heading to lower case;
    2. Removing any character that can't be used in a Python identifier
    3. Replacing all whitespace with "_"
    4. Prepending ``_`` if the first character is a digit.

    Examples:

    * 'Heading 1' -> 'heading_1'
    * 'Heading - Title' -> 'heading_title'
    * 'Heading!' -> 'heading'
    * '1 Heading' -> '_1_heading'
    * '你好' -> '你好'

    :param heading: The column heading.
    :returns: The accessor derived from the heading.
    :raises ValueError: If the heading cannot be converted into an accessor.
    """
    value = WHITESPACE.sub(
        " ",
        NON_ACCESSOR_CHARS.sub("", heading.lower()),
    ).replace(" ", "_")

    try:
        if value[0].isdigit():
            value = f"_{value}"
    except IndexError:
        raise ValueError(
            f"Unable to automatically generate accessor from heading {heading!r}."
        )

    return value


def build_accessors(
    headings: list[str],
    accessors: list[str | None] | dict[str, str] | None,
) -> list[str]:
    """Convert a list of headings (with accessor overrides) to a finalised list of
    accessors.

    :param headings: The list of headings.
    :param accessors: The list of accessor overrides. Can be specified as:

        * A list the same length as headings. Each entry in the list is a a string that
          is the override name for the accessor, or :any:`None` if the default accessor
          for the heading at that index should be used.
        * A dictionary mapping heading names to accessor names. If a heading name isn't
          present in the dictionary, the default accessor will be used.

    :returns: The final list of accessors.
    """
    if accessors:
        if isinstance(accessors, dict):
            result = [
                accessors[h] if h in accessors else to_accessor(h) for h in headings
            ]
        else:
            if len(headings) != len(accessors):
                raise ValueError("Number of accessors must match number of headings")

            result = [
                a if a is not None else to_accessor(h)
                for h, a in zip(headings, accessors)
            ]
    else:
        result = [to_accessor(h) for h in headings]

    return result
