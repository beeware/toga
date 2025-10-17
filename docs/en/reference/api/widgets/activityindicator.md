# ActivityIndicator

A small animated indicator showing activity on a task of indeterminate length, usually rendered as a "spinner" animation.

/// tab | macOS

![/reference/images/activityindicator-cocoa.png](/reference/images/activityindicator-cocoa.png){ width="100" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux (GTK)

![/reference/images/activityindicator-gtk.png](/reference/images/activityindicator-gtk.png){ width="100" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux (Qt)

![An ActivityIndicator widget, running on Toga's Qt backend](/reference/images/activityindicator-qt.png){ width="100" }

/// caption

///

///

/// tab | Windows

![/reference/images/activityindicator-winforms.png](/reference/images/activityindicator-winforms.png){ width="100" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android

![/reference/images/activityindicator-android.png](/reference/images/activityindicator-android.png){ width="100" }

/// caption

///

///

/// tab | iOS

![/reference/images/activityindicator-iOS.png](/reference/images/activityindicator-iOS.png){ width="100" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Web {{ beta_support }}

![/reference/images/activityindicator-web.png](/reference/images/activityindicator-web.png){ width="100" }

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

indicator = toga.ActivityIndicator()

# Start the animation
indicator.start()

# Stop the animation
indicator.stop()
```

## Notes

- The ActivityIndicator will always take up a fixed amount of physical space in a layout. However, the widget will not be visible when it is in a "stopped" state.

## Reference

::: toga.ActivityIndicator
