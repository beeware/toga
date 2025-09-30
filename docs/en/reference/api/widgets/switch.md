# Switch

A clickable button with two stable states: True (on, checked); and False (off, unchecked). The button has a text label.

/// tab | macOS

![/reference/images/switch-cocoa.png](/reference/images/switch-cocoa.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux

![/reference/images/switch-gtk.png](/reference/images/switch-gtk.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Windows

![/reference/images/switch-winforms.png](/reference/images/switch-winforms.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android

![/reference/images/switch-android.png](/reference/images/switch-android.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | iOS

![/reference/images/switch-iOS.png](/reference/images/switch-iOS.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Web {{ beta_support }}

![/reference/images/switch-web.png](/reference/images/switch-web.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Textual {{ not_supported }}

Not supported

///

## Usage

```python
import toga

switch = toga.Switch()

# What is the current state of the switch?
print(f"The switch is {switch.value}")
```

## Notes

- The button and the label are considered a single widget for layout purposes.
- The visual appearance of a Switch is not guaranteed. On some platforms, it will render as a checkbox. On others, it will render as a physical "switch" whose position (and color) indicates if the switch is active. When rendered as a checkbox, the label will appear to the right of the checkbox. When rendered as a switch, the label will be left-aligned, and the switch will be right-aligned.
- You should avoid setting a `height` style property on Switch widgets. The rendered height of the Switch widget will be whatever the platform style guide considers appropriate; explicitly setting a `height` for the widget can lead to widgets that have a distorted appearance.
- On macOS, the text color of the label cannot be set directly; any `color` style directive will be ignored.

## Reference

::: toga.Switch

::: toga.widgets.switch.OnChangeHandler
