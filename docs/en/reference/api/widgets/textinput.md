# TextInput

A widget for the display and editing of a single line of text.

/// tab | macOS

![/reference/images/textinput-cocoa.png](/reference/images/textinput-cocoa.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux

![/reference/images/textinput-gtk.png](/reference/images/textinput-gtk.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Windows

![/reference/images/textinput-winforms.png](/reference/images/textinput-winforms.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android

![/reference/images/textinput-android.png](/reference/images/textinput-android.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | iOS

![/reference/images/textinput-iOS.png](/reference/images/textinput-iOS.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Web {{ beta_support }}

![/reference/images/textinput-web.png](/reference/images/textinput-web.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Textual {{ beta_support }}

Screenshot not available

///

## Usage

```python
import toga

text_input = toga.TextInput()
text_input.value = "Jane Developer"
```

The input can be provided a placeholder value - this is a value that will be displayed to the user as a prompt for appropriate content for the widget. This placeholder will only be displayed if the widget has no content; as soon as a value is provided (either by the user, or programmatically), the placeholder content will be hidden.

The input can also be provided a list of [`validators`][]. A validator is a function that will be invoked whenever the content of the input changes. The function should return `None` if the current value of the input is valid; if the current value is invalid, it should return an error message. When `on_change` is invoked, the field will automatically be validated based on specified validators.

## Notes

- Although an error message is provided when validation fails, Toga does not guarantee that this error message will be displayed to the user.
- Winforms does not support the use of partially or fully transparent colors for the TextInput background. If a color with an alpha value is provided (including `TRANSPARENT`), the alpha channel will be ignored. A `TRANSPARENT` background will be rendered as white.
- On Winforms, if a TextInput is given an explicit height, the rendered widget will not expand to fill that space. The widget will have the fixed height determined by the font used on the widget. In general, you should avoid setting a `height` style property on TextInput widgets.

## Reference

::: toga.TextInput

::: toga.widgets.textinput.OnChangeHandler

::: toga.widgets.textinput.OnConfirmHandler

::: toga.widgets.textinput.OnGainFocusHandler

::: toga.widgets.textinput.OnLoseFocusHandler
