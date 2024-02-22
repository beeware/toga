try:
    # Try to import js from the PyScript namespace
    import js
except ModuleNotFoundError:
    # To ensure the code can be imported, provide a js symbol as a fallback
    js = None


try:
    # Try to import pyodide from the PyScript namespace
    import pyodide
except ModuleNotFoundError:
    # To ensure the code can be imported, provide a pyodide symbol as a fallback
    pyodide = None


create_proxy = pyodide.ffi.create_proxy if pyodide else lambda f: f


def create_element(
    tag,
    id=None,
    classes=None,
    style=None,
    disabled=False,
    content=None,
    children=None,
    **properties,
):
    """Utility method for creating DOM elements.

    :param tag: The HTML tag of the element to create
    :param id: (Optional) The ID of the new element
    :param classes: (Optional) A list of classes to attach to the new element.
    :param style: (Optional) The CSS style for the element.
    :param disabled: (Optional) Should the element be disabled at time of
        creation? (Default: False)
    :param content: (Optional) The innerHTML content of the element.
    :param children: (Optional) A list of direct descendents to add to the
        element.
    :param properties: Any additional properties that should be set. These
        *must* be HTML DOM properties (e.g., ``readOnly``); they cannot be
        events or methods.
    :returns: A newly created DOM element.
    """
    element = js.document.createElement(tag)

    if id:
        element.id = id

    if classes:
        for klass in classes:
            element.classList.add(klass)

    if style:
        element.style = style

    if disabled:
        element.setAttribute("disabled", "")

    for attr, value in properties.items():
        element.setAttribute(attr.replace("_", "-"), value)

    if content:
        element.innerHTML = content

    if children:
        for child in children:
            element.appendChild(child)

    return element
