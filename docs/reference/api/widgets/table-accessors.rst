The attribute names used on each row (called "accessors") are created automatically from
the headings, by:

1. Converting the heading to lower case
2. Removing any character that can't be used in a Python identifier
3. Replacing all whitespace with ``_``
4. Prepending ``_`` if the first character is a digit
