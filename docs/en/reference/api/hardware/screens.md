# Screen

A representation of a screen attached to a device.

::: {.rst-class}
widget-support
:::

::: {.csv-filter header-rows="1" file="../../data/widgets_by_platform.csv" included_cols="4,5,6,7,8,9,10" include="{0: '^Screen$'}"}
Availability (`Key <api-status-key>`{.interpreted-text role="ref"})
:::

## Usage

An app will always have access to at least one screen. The
`toga.App.screens`{.interpreted-text role="any"} attribute will return
the list of all available screens; the screen at index 0 will be the
"primary" screen. Screen sizes and positions are given in CSS pixels.

``` python
# Print the size of the primary screen.
print(my_app.screens[0].size)

# Print the identifying name of the second screen
print(my_app.screens[1].name)
```

## Notes

- When using the GTK backend under Wayland, the screen at index 0 may
  not be the primary screen. This because the separation of concerns
  enforced by Wayland makes determining the primary screen unreliable.

## Reference

::: {.autoclass}
toga.screens.Screen
:::
