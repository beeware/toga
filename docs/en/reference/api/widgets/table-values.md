The value provided by an accessor is interpreted as follows:

- If the value is a `Widget`{.interpreted-text role="any"}, that widget
  will be displayed in the cell. Note that this is currently a beta API:
  see the Notes section.
- If the value is a `tuple`{.interpreted-text role="any"}, it must have
  two elements: an icon, and a second element which will be interpreted
  as one of the options below.
- If the value is `None`, then `missing_value` will be displayed.
- Any other value will be converted into a string. If an icon has not
  already been provided in a tuple, it can also be provided using the
  value's `icon` attribute.

Icon values must either be an `Icon`{.interpreted-text role="any"},
which will be displayed on the left of the cell, or `None` to display no
icon.
