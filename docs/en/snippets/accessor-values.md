<!-- rumdl-disable-line MD041 -->

Accessor names (whether explicitly provided, or automatically generated from the header names) should be unique. If they are not, column data will be duplicated, as Toga has no way to tell which version of an accessor to use when populating data for a column.

The value provided by an accessor is interpreted as follows:

- If the value is a [Widget][], that widget will be displayed in the cell. Note that this is currently a beta API: see the Notes section.
- If the value is a [`tuple`][], it must have two elements: an icon, and a second element which will be interpreted as one of the options below. A tuple of any other length will raise an error.
- If the value is `None`, then `missing_value` will be displayed.
- Any other value will be converted into a string. If an icon has not already been provided in a tuple, it can also be provided using the value's `icon` attribute.

Icon values must either be an [Icon][], which will be displayed on the left of the cell, or `None` to display no icon.
