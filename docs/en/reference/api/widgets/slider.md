# Slider

A widget for selecting a value within a range. The range is shown as a horizontal line, and the selected value is shown as a draggable marker.

/// tab | macOS

![/reference/images/slider-cocoa.png](/reference/images/slider-cocoa.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux

![/reference/images/slider-gtk.png](/reference/images/slider-gtk.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Windows

![/reference/images/slider-winforms.png](/reference/images/slider-winforms.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android

![/reference/images/slider-android.png](/reference/images/slider-android.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | iOS

![/reference/images/slider-iOS.png](/reference/images/slider-iOS.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Web

![/reference/images/slider-web.png](/reference/images/slider-web.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Textual {{ not_supported }}

Not supported

///

## Usage

A slider can either be continuous (allowing any value within the range), or discrete (allowing a fixed number of equally-spaced values). For example:

```python
import toga

def my_callback(slider):
    print(slider.value)

# Continuous slider, with an event handler.
toga.Slider(min=-5, max=10, value=7, on_change=my_callback)

# Discrete slider, accepting the values [0, 1.5, 3, 4.5, 6, 7.5].
toga.Slider(min=0, max=7.5, tick_count=6)
```

## Reference

::: toga.Slider

::: toga.widgets.slider.OnChangeHandler

::: toga.widgets.slider.OnPressHandler

::: toga.widgets.slider.OnReleaseHandler
