# Button

A button that can be pressed or clicked.

/// tab | macOS

![/reference/images/button-cocoa.png](/reference/images/button-cocoa.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux

![/reference/images/button-gtk.png](/reference/images/button-gtk.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Windows

![/reference/images/button-winforms.png](/reference/images/button-winforms.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android

![/reference/images/button-android.png](/reference/images/button-android.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | iOS

![/reference/images/button-iOS.png](/reference/images/button-iOS.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Web {{ beta_support }}

![/reference/images/button-web.png](/reference/images/button-web.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Textual {{ beta_support }}

Screenshot not available

///

## Usage

A button has a text label, or an icon (but not both). If an icon is specified, it will be resized to a size appropriate for the platform. A handler can be associated with button press events.

```python
import toga

def my_callback(button):
    # handle event
    pass

button = toga.Button("Click me", on_press=my_callback)

icon_button = toga.Button(icon=toga.Icon("resources/my_icon"), on_press=my_callback)
```

## Notes

- A background color of `TRANSPARENT` will be treated as a reset of the button to the default system color.
- On macOS, the button text color cannot be set directly; any `color` style directive will be ignored. The text color is automatically selected by the platform to contrast with the background color of the button.

## Reference

::: toga.Button

::: toga.widgets.button.OnPressHandler
