{{ component_header("Switch", width=300) }}

## Usage

A `Switch`'s button has a text label, and two states: `True` (on, checked); and `False` (off, unchecked).

```python
import toga

switch = toga.Switch("Switch label")

# What is the current state of the switch?
print(f"The switch is {switch.value}")
```

A `Switch` may render as either a checkbox or a toggle. The default "role" of the switch is up to platform defaults, but you can customize it using the `role` parameter.

Some platforms encourage one appearance for "major" toggles, such as a switch that controls a group of settings, and a different appearance for "minor" toggles, such as ones you might use when displaying a list of several equally important options. To make your app fit most into the user's platform, specify `SwitchRole.MAJOR` or `SwitchRole.MINOR` in the `role` parameter when creating a `Switch`.

```python
from toga.constants import SwitchRole

toga.Box(children=[
    toga.Switch("A major switch", role=SwitchRole.MAJOR),
    toga.Switch("A minor switch", role=SwitchRole.MINOR)
])
```

If you want to force the appearance of a `Switch` as a checkbox or toggle switch, you may use `SwitchRole.CHECKBOX` or `SwitchRole.SWITCH`. However, this is not a guarantee, as some platforms only support one appearance and will not respect this choice.

## Notes

- The button and the label are considered a single widget for layout purposes.
- The `role` parameter is currently only supported on macOS. On other platforms, the appearance of a `Switch` is not guaranteed.
- You should avoid setting a `height` style property on `Switch` widgets. The rendered height of the `Switch` widget will be whatever the platform style guide considers appropriate; explicitly setting a `height` for the widget can lead to widgets that have a distorted appearance.
- On macOS, the text color of the label cannot be set directly; any `color` style directive will be ignored.

## Reference

::: toga.Switch

::: toga.widgets.switch.OnChangeHandler
