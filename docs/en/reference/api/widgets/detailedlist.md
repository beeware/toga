# DetailedList

/// tab | macOS

![/reference/images/detailedlist-cocoa.png](/reference/images/detailedlist-cocoa.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | GTK

![/reference/images/detailedlist-gtk.png](/reference/images/detailedlist-gtk.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Qt {{ not_supported }}

Not supported

///

/// tab | Windows {{ beta_support }}

![/reference/images/detailedlist-winforms.png](/reference/images/detailedlist-winforms.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android

![/reference/images/detailedlist-android.png](/reference/images/detailedlist-android.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | iOS

![/reference/images/detailedlist-iOS.png](/reference/images/detailedlist-iOS.png){ width="450" }

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

The simplest way to create a DetailedList is to pass a list of dictionaries, with each dictionary containing three keys: `icon`, `title`, and `subtitle`:

```python
import toga

table = toga.DetailedList(
    data=[
        {
           "icon": toga.Icon("icons/arthur"),
           "title": "Arthur Dent",
           "subtitle": "Where's the tea?"
        },
        {
           "icon": toga.Icon("icons/ford"),
           "title": "Ford Prefect",
           "subtitle": "Do you know where my towel is?"
        },
        {
           "icon": toga.Icon("icons/tricia"),
           "title": "Tricia McMillan",
           "subtitle": "What planet are you from?"
        },
    ]
)
```

If you want to customize the keys used in the dictionary, you can do this by providing an `accessors` argument to the DetailedList when it is constructed. `accessors` is a tuple containing the attributes that will be used to provide the icon, title, and subtitle, respectively:

```python
import toga

table = toga.DetailedList(
    accessors=("picture", "name", "quote"),
    data=[
        {
           "picture": toga.Icon("icons/arthur"),
           "name": "Arthur Dent",
           "quote": "Where's the tea?"
        },
        {
           "picture": toga.Icon("icons/ford"),
           "name": "Ford Prefect",
           "quote": "Do you know where my towel is?"
        },
        {
           "picture": toga.Icon("icons/tricia"),
           "name": "Tricia McMillan",
           "quote": "What planet are you from?"
        },
    ]
)
```

If the value provided by the title or subtitle accessor is `None`, or the accessor isn't defined, the `missing_value` will be displayed. Any other value will be converted into a string.

The icon accessor should return an [`Icon`][toga.Icon]. If it returns `None`, or the accessor isn't defined, then no icon will be displayed, but space for the icon will remain in the layout.

Items in a DetailedList can respond to a primary and secondary action. On platforms that use swipe interactions, the primary action will be associated with "swipe left", and the secondary action will be associated with "swipe right". Other platforms may implement the primary and secondary actions using a different UI interaction (e.g., a right-click context menu). The primary and secondary actions will only be enabled in the DetailedList UI if a handler has been provided.

By default, the primary and secondary action will be labeled as "Delete" and "Action", respectively. These names can be overridden by providing a `primary_action` and `secondary_action` argument when constructing the DetailedList. Although the primary action is labeled "Delete" by default, the DetailedList will not perform any data deletion as part of the UI interaction. It is the responsibility of the application to implement any data deletion behavior as part of the `on_primary_action` handler.

The DetailedList as a whole can also respond to a refresh UI action. This is usually implemented as a "pull down" action, such as you might see on a social media timeline. This action will only be enabled in the UI if an `on_refresh` handler has been provided.

## Notes

- The iOS Human Interface Guidelines differentiate between "Normal" and "Destructive" actions on a row. Toga will interpret any action with a name of "Delete" or "Remove" as destructive, and will render the action appropriately.
- The WinForms implementation currently uses a column layout similar to [`Table`][toga.Table], and does not support the primary, secondary or refresh actions.
- Using DetailedList on Android requires the AndroidX SwipeRefreshLayout widget in your project's Gradle dependencies. Ensure your app declares a dependency on `androidx.swiperefreshlayout:swiperefreshlayout:1.1.0` or later.

## Reference

::: toga.DetailedList

::: toga.widgets.detailedlist.OnPrimaryActionHandler

::: toga.widgets.detailedlist.OnSecondaryActionHandler

::: toga.widgets.detailedlist.OnRefreshHandler

::: toga.widgets.detailedlist.OnSelectHandler
