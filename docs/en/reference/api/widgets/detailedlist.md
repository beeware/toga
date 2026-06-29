{{ component_header("DetailedList", width=450) }}

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

Items in a DetailedList will respond to a primary and secondary action if the `on_primary_action` and `on_secondary_action` handlers are set:

* On **Android**, a long press displays a menu with the primary and secondary actions.
* On **iOS**, swiping left triggers the primary action, and swiping right triggers the secondary action.
* On **GTK**, a right click displays buttons for the primary and secondary actions.
* On **macOS** and **Windows**, a right click displays a context menu with the primary and secondary actions.
* On **Qt**, the primary and secondary actions are displayed as standalone buttons.

By default, the primary and secondary action will be labeled as "Delete" and "Action", respectively. These names can be overridden by providing a `primary_action` and `secondary_action` argument when constructing the DetailedList. Although the primary action is labeled "Delete" by default, the DetailedList will not perform any data deletion as part of the UI interaction. It is the responsibility of the application to implement any data deletion behavior as part of the `on_primary_action` handler.

The DetailedList as a whole will also respond to a refresh UI action if an `on_refresh` handler is set:

* On **Android**, **iOS** and **macOS**, pulling down at the top of the list triggers a refresh.
* On **Qt**, a button bar displays a refresh button.
* On **GTK**, a floating refresh button is displayed when scrolled to the top.
* On **Windows**, a right click displays a context menu with a refresh option.

## Notes

* The iOS Human Interface Guidelines differentiate between "Normal" and "Destructive" actions on a row. Toga will interpret any action with a name of "Delete" or "Remove" as destructive, and will render the action appropriately.
* Using DetailedList on Android requires the AndroidX SwipeRefreshLayout widget in your project's Gradle dependencies. Ensure your app declares a dependency on `androidx.swiperefreshlayout:swiperefreshlayout:1.1.0` or later.

## Reference

::: toga.DetailedList

::: toga.widgets.detailedlist.OnPrimaryActionHandler

::: toga.widgets.detailedlist.OnSecondaryActionHandler

::: toga.widgets.detailedlist.OnRefreshHandler

::: toga.widgets.detailedlist.OnSelectHandler
