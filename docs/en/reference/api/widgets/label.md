# Label

A text label for annotating forms or interfaces.

/// tab | macOS

![/reference/images/label-cocoa.png](/reference/images/label-cocoa.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux

![/reference/images/label-gtk.png](/reference/images/label-gtk.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Windows

![/reference/images/label-winforms.png](/reference/images/label-winforms.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android

![/reference/images/label-android.png](/reference/images/label-android.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | iOS

![/reference/images/label-iOS.png](/reference/images/label-iOS.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Web {{ beta_support }}

![/reference/images/label-web.png](/reference/images/label-web.png){ width="300" }

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

label = toga.Label("Hello world")
```

## Notes

- Winforms does not support a text alignment value of `JUSTIFIED`. If this alignment value is used, the label will default to left alignment.

## Reference

::: toga.Label
