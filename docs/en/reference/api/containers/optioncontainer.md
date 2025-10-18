# OptionContainer

A container that can display multiple labeled tabs of content.

/// tab | macOS

![/reference/images/optioncontainer-cocoa.png](/reference/images/optioncontainer-cocoa.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux (GTK)

![/reference/images/optioncontainer-gtk.png](/reference/images/optioncontainer-gtk.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux (Qt) {{ not_supported }}

Not supported

///

/// tab | Windows

![/reference/images/optioncontainer-winforms.png](/reference/images/optioncontainer-winforms.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android

![/reference/images/optioncontainer-android.png](/reference/images/optioncontainer-android.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | iOS

![/reference/images/optioncontainer-iOS.png](/reference/images/optioncontainer-iOS.png){ width="450" }

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

The content of an OptionContainer is a list of widgets that will form discrete tabs in the display. Each tab can be identified by a label, and, optionally, an icon. This list of content can be modified after initial construction:

```python
import toga

pizza = toga.Box()
pasta = toga.Box()

# Create 2 initial tabs; one with an icon, and one without.
container = toga.OptionContainer(
    content=[("Pizza", pizza), ("Pasta", pasta, toga.Icon("pasta"))]
)

# Add another tab of content, without an icon.
salad = toga.Box()
container.content.append("Salad", salad)

# Add another tab of content, with an icon
icecream = toga.Box()
container.content.append("Ice Cream", icecream, toga.Icon("icecream"))
```

OptionContainer content can also be specified by using [`toga.OptionItem`][] instances instead of tuples. This enables you to be explicit when setting an icon or enabled status; it also allows you to set the initial enabled status *without* setting an icon:

```python
import toga

pizza = toga.Box()
pasta = toga.Box()

# Create 2 initial tabs; one with an icon, and one without.
container = toga.OptionContainer(
    content=[`
      toga.OptionItem("Pizza", pizza),
      toga.OptionItem("Pasta", pasta, icon=toga.Icon("pasta"))
    ]
)

# Add another tab of content, initially disabled, without an icon.
salad = toga.Box()
container.content.append(toga.OptionItem("Salad", salad, enabled=False))
```

When retrieving or deleting items, or when specifying the currently selected item, you can specify an item using:

- The index of the item in the list of content:

    ```python
    # Insert a new second tab
    container.content.insert(1, "Soup", toga.Box())
    # Make the third tab the currently active tab
    container.current_tab = 2
    # Delete the second tab
    del container.content[1]
    ```

- The string label of the tab:

    ```python
    # Insert a tab at the index currently occupied by a tab labeled "Pasta"
    container.content.insert("Pasta", "Soup", toga.Box())
    # Make the tab labeled "Pasta" the currently active tab
    container.current_tab = "Pasta"
    # Delete tab labeled "Pasta"
    del container.content["Pasta"]
    ```

- A reference to an [`toga.OptionItem`][]:

    ```python
    # Get a reference to the "Pasta" tab
    pasta_tab = container.content["Pasta"]
    # Insert content at the index currently occupied by the pasta tab
    container.content.insert(pasta_tab, "Soup", toga.Box())
    # Make the pasta tab the currently active tab
    container.current_tab = pasta_tab
    # Delete the pasta tab
    del container.content[pasta_tab]
    ```

## System requirements

- Using OptionContainer on Android requires the Material package in your project's Gradle dependencies. Ensure your app declares a dependency on `com.google.android.material:material:1.12.0` or later.

## Notes

- The use of icons on tabs varies between platforms. If the platform requires icons, and no icon is provided, a default icon will be used. If the platform does not support icons, any icon provided will be ignored, and requests to retrieve the icon will return `None`.
- The behavior of disabled tabs varies between platforms. Some platforms will display the tab, but put it in an unselectable state; some will hide the tab. A hidden tab can still be referenced by index - the tab index refers to the logical order, not the visible order.
- iOS can only display 5 tabs. If there are more than 5 visible tabs in an OptionContainer, the last item will be converted into a "More" option that will allow the user to select the additional items. While the "More" menu is displayed, the current tab will return as `None`.
- Android can only display 5 tabs. The API will allow you to add more than 5 tabs, and will allow you to programmatically control tabs past the 5-item limit, but any tabs past the limit will not be displayed or be selectable by user interaction. If the OptionContainer has more than 5 tabs, and one of the visible tabs is removed, one of the previously unselectable tabs will become visible and selectable.
- iOS allows the user to rearrange icons on an OptionContainer. When referring to tabs by index, user re-ordering is ignored; the logical order as configured in Toga itself is used to identify tabs.
- Icons for iOS OptionContainer tabs should be 25x25px alpha masks.
- Icons for Android OptionContainer tabs should be 24x24px alpha masks.

## Reference

::: toga.OptionContainer

::: toga.OptionItem

::: toga.widgets.optioncontainer.OptionList

::: toga.widgets.optioncontainer.OptionItem

::: toga.widgets.optioncontainer.OnSelectHandler

::: toga.widgets.optioncontainer.OptionContainerContentT
