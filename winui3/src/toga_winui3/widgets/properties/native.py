def get_attribute_base_recursive(cls, attribute):
    for parent in cls.__bases__:
        if hasattr(parent, attribute):
            return parent

        branch_result = get_attribute_base_recursive(parent, attribute)
        if branch_result is not None:
            return branch_result

    return None


def get_attribute_base(cls, attribute):
    if hasattr(cls, attribute):
        return cls
    else:
        return get_attribute_base_recursive(cls, attribute)


class NativeProperties:
    """Sets the native properties of a widget and clears dependency properties.

    In WinUI 3, a there is a special type of property called a 'denpendency property'.
    These properties are characterised by being dependent on values of the application
    which can change e.g. DPI, darkmode theme. When a dependency property is manually
    set to a value, it can lose the ability to listen to these changes.

    Using this class to set a dependency property to None resets the property to the
    default value and restores the ability to listen to changes.
    """

    def __init__(self, widget):
        self._widget = widget

    def __setattr__(self, name, value):
        """Sets the native property value for a name with a capital first character."""
        if not name[0].isupper():
            super().__setattr__(name, value)
            return

        self.set_native_property(name, value)

    def set_native_property(self, name, value):
        native_instance = self._widget.native

        # This codeblock shouldn't be accessed under normal operations, so use no cover.
        if not hasattr(native_instance, name):  # pragma: no cover
            raise AttributeError(f"{native_instance} has no attribute named {name}.")

        # For non-None values, set the property as normal.
        if value is not None:
            setattr(native_instance, name, value)
            return

        native_cls = type(native_instance)
        dependency_property = name + "Property"
        dependency_ancestor = get_attribute_base(native_cls, dependency_property)

        if dependency_ancestor is not None:
            # Clear the dependency property.
            dependency_attribute = getattr(dependency_ancestor, dependency_property)
            native_instance.ClearValue(dependency_attribute)
        else:
            # Fallback to the usual setattr for non-dependeny properties.
            setattr(native_instance, name, value)
