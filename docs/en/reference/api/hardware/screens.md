# Screen

A representation of a screen attached to a device.

Availability ([Key][api-status-key])  <!-- rumdl-disable-line MD013 -->
{: .availability-title }

{{ pd_read_csv("../../data/widgets_by_platform.csv", na_filter=False, usecols=[4,5,6,7,8,9,10])[pd_read_csv("../../data/widgets_by_platform.csv")[["ComponentName"]].isin(["Screen"]).all(axis=1)] | convert_to_md_table }}

## Usage

An app will always have access to at least one screen. The [`toga.App.screens`][] attribute will return the list of all available screens; the screen at index 0 will be the "primary" screen. Screen sizes and positions are given in CSS pixels.

```python
# Print the size of the primary screen.
print(my_app.screens[0].size)

# Print the identifying name of the second screen
print(my_app.screens[1].name)
```

## Notes

- When using the GTK backend under Wayland, the screen at index 0 may not be the primary screen. This because the separation of concerns enforced by Wayland makes determining the primary screen unreliable.

## Reference

::: toga.screens.Screen
