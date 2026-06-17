{{ component_header("Screen") }}

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
