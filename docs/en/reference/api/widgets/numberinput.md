# NumberInput

A text input that is limited to numeric input.

/// tab | macOS

![/reference/images/numberinput-cocoa.png](/reference/images/numberinput-cocoa.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | GTK

![/reference/images/numberinput-gtk.png](/reference/images/numberinput-gtk.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Qt {{ not_supported }}

Not supported

///

/// tab | Windows

![/reference/images/numberinput-winforms.png](/reference/images/numberinput-winforms.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android

![/reference/images/numberinput-android.png](/reference/images/numberinput-android.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | iOS

![/reference/images/numberinput-iOS.png](/reference/images/numberinput-iOS.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Web {{ not_supported }}

Not supported

///

/// tab | Textual {{ not_supported }}

Not supported

///

## Usage

```python
import toga

widget = toga.NumberInput(min=1, max=10, step=0.001)
widget.value = 2.718
```

NumberInput's properties can accept [`Decimal`][decimal], [`int`][], [`float`][], or [`str`][] containing numbers, but they always return [`Decimal`][decimal] objects to ensure precision is retained.

## Reference

::: toga.NumberInput

::: toga.widgets.numberinput.OnChangeHandler

::: toga.widgets.numberinput.NumberInputT
