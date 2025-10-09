# Keys

A symbolic representation of keys used for keyboard shortcuts.

Most keys have a constant that matches the text on the key, or the name of the key if the text on the key isn't a legal Python identifier.

However, due to differences between platforms, there's no representation of "modifier" keys like Control, Command, Option, or the Windows Key. Instead, Toga provides three generic modifier constants, and maps those to the modifier keys, matching the precedence with which they are used on the underlying platforms:

| Platform | [MOD_1][toga.Key.MOD_1] | [MOD_2][toga.Key.MOD_2] | [MOD_3][toga.Key.MOD_3] |
|----------|-------------------------|-------------------------|-------------------------|
| Linux    | Control                 | Alt                     | Tux/Windows/Meta        |
| macOS    | Command (⌘)             | Option                  | Control (^)             |
| Windows  | Control                 | Alt                     | Not supported           |

Key combinations can be expressed by combining multiple `Key` values with the `+` operator.

```python
from toga import Key

just_an_a = Key.A
shift_a = Key.SHIFT + Key.A
# Windows/Linux - Control-Shift-A:
# macOS - Command-Shift-A:
modified_shift_a = Key.MOD_1 + Key.SHIFT + Key.A
```

The order of addition is not significant. `Key.SHIFT + Key.A` and `Key.A + Key.SHIFT` will produce the same key representation.

## Reference

::: toga.Key
    options:
        show_if_no_docstring: true
        members_order: source
        separate_signature: false
        show_labels: false
        show_private_members: true
