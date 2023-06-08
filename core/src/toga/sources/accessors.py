import re

NON_ACCESSOR_CHARS = re.compile(r"[^\w ]")
WHITESPACE = re.compile(r"\s+")


def to_accessor(heading):
    """Convert a human-readable heading into a data attribute accessor.

    This won't be infallible; for ambiguous cases, you'll need to manually
    specify the accessors.

    Examples:
        'Heading 1' -> 'heading_1'
        'Heading - Title' -> 'heading_title'
        'Heading!' -> 'heading'

    Args:
        heading (``str``): The column heading.

    Returns:
        the accessor derived from the heading.
    """
    value = WHITESPACE.sub(
        " ",
        NON_ACCESSOR_CHARS.sub("", heading.lower()),
    ).replace(" ", "_")

    if len(value) == 0 or value[0].isdigit():
        raise ValueError(
            f"Unable to automatically generate accessor from heading '{heading}'."
        )

    return value


def build_accessors(headings, accessors):
    """Convert a list of headings (with accessor overrides) to a finalised list of
    accessors.

    Args:
        headings: a list of strings to be used as headings
        accessors: the accessor overrides. Can be:
         - A list, same length as headings. Each entry is
           a string providing the override name for the accessor,
           or None, indicating the default accessor should be used.
         - A dictionary from the heading names to the accessor. If
           a heading name isn't present in the dictionary, the default
           accessor will be used
         - Otherwise, a final list of ready-to-use accessors.

    Returns:
        A finalised list of accessors.
    """
    if accessors:
        if headings is None:
            if not isinstance(accessors, (list, tuple)):
                raise TypeError(
                    "When no headings are provided, accessors must be a list or tuple"
                )
            if not all(accessors):
                raise ValueError(
                    "When no headings are provided, all accessors must be defined"
                )
            result = accessors
        elif isinstance(accessors, dict):
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
        if headings:
            result = [to_accessor(h) for h in headings]
        else:
            raise ValueError("Either headings or accessors must be provided")

    if len(result) != len(set(result)):
        raise ValueError("Data accessors are not unique.")

    return result
