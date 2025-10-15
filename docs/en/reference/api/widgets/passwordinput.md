# PasswordInput

A widget to allow the entry of a password. Any value typed by the user will be obscured, allowing the user to see the number of characters they have typed, but not the actual characters.

/// tab | macOS

![/reference/images/passwordinput-cocoa.png](/reference/images/passwordinput-cocoa.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | GTK

![/reference/images/passwordinput-gtk.png](/reference/images/passwordinput-gtk.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Qt {{ not_supported }}

Not supported

///

/// tab | Windows

![/reference/images/passwordinput-winforms.png](/reference/images/passwordinput-winforms.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android

![/reference/images/passwordinput-android.png](/reference/images/passwordinput-android.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | iOS

![/reference/images/passwordinput-iOS.png](/reference/images/passwordinput-iOS.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Web

![/reference/images/passwordinput-web.png](/reference/images/passwordinput-web.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Textual {{ not_supported }}

Not supported

///

## Usage

The `PasswordInput` is functionally identical to a [`TextInput`][toga.TextInput], except for how the text is displayed. All features supported by [`TextInput`][toga.TextInput] are also supported by PasswordInput.

```python
import toga

password = toga.PasswordInput()
```

## Notes

- Winforms does not support the use of partially or fully transparent colors for the PasswordInput background. If a color with an alpha value is provided (including `TRANSPARENT`), the alpha channel will be ignored. A `TRANSPARENT` background will be rendered as white.
- On Winforms, if a PasswordInput is given an explicit height, the rendered widget will not expand to fill that space. The widget will have the fixed height determined by the font used on the widget. In general, you should avoid setting a `height` style property on PasswordInput widgets.

## Reference

::: toga.PasswordInput
