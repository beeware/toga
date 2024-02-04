import json
import toga
import inspect
from toga.style import Pack
from xml.etree import ElementTree


def parse_node_as_dict(node):
    return {
        child.tag: parse_node_as_dict(child) if len(child) else child.text or ""
        for child in node
    }


def parse_attribute(app, element):
    # If attribute is a list item and has children, parse it as dict
    if element.tag == "item" and len(element):
        return {element.tag: parse_node_as_dict(element)}

    # Get attributes
    attributes = {**element.attrib}
    attributes[element.tag] = []

    # Get text inside node
    if element.text.strip():
        attributes[element.tag].append(element.text)

    # For each child
    for child in element:
        # Parse child attribute
        ele_attr = parse_attribute(app, child)[child.tag]
        if type(ele_attr) != list:
            ele_attr = [ele_attr]

        # Save attribute
        attributes[element.tag] = [*attributes[element.tag], *ele_attr]

    return attributes


def get_element_attrs(app, element):
    # Object attributes
    attributes = {**element.attrib}

    # If there is text inside the tag, save it as attribute
    if element.text and element.text.strip():
        attributes["text"] = element.text

    # Checking style and events props
    for key, value in element.attrib.items():
        # Handling events
        if key.startswith("on_"):
            # Handling inside class functions pointers
            if value.startswith("."):
                attributes[key] = getattr(app, value[1:])
            continue

        # Handling numeric values
        if value.isnumeric():
            if "." in value:
                attributes[key] = float(value)
            else:
                attributes[key] = int(value)
            continue

        # Handling booleans
        if value.strip() == "true":
            attributes[key] = True
            continue

        if value.strip() == "false":
            attributes[key] = False
            continue

        # Handling styles
        if key == "style":
            style = {}
            for item in value.split(";"):
                # Need the strip in case ";" is set at the end of style
                if item.strip():
                    a, v = item.split(":")
                    style[a.strip()] = v.strip()
            attributes["style"] = Pack(**style)
            continue

        # Handling app variables ref
        if value.startswith("."):
            attributes[key] = getattr(app, value[1:])
            continue

    return attributes


def element_to_class(element_tag, attributes):
    # Get TogaElement class
    klass = getattr(toga, element_tag)

    # Filter initial attributes
    init_args = {
        key: value
        for key, value in attributes.items()
        if key in inspect.getfullargspec(klass).args
    }

    # Creatting element instance
    instance = klass(**init_args)

    # Setting attributes all attributes
    for key, value in attributes.items():
        try:
            # Sometimes attr has no setter or it is repeated (content/children/image)
            # So this try is a hacky way to solve it
            setattr(instance, key, value)
        except:
            pass

    return instance


def parse_element(app, element):
    # Class args
    attributes = get_element_attrs(app, element)
    # Children elements
    children = []

    # Traversing children elements
    for child in element:
        # Lowercase element tag means "attribute"
        if not child.tag.islower():
            # If tag is a TogaElement, parse child and add it to children array
            children.append(parse_element(app, child))
            continue

        attributes = {**attributes, **parse_attribute(app, child)}

    first_child = children[0] if len(children) else children

    attributes["image"] = first_child  # For ImageView component

    # Children and content for some widgets are list, for others an unique child
    # So we are trying with only one child and on except we try with the list variant
    attributes["content"] = first_child
    attributes["children"] = first_child

    try:
        instance = element_to_class(element.tag, attributes)
    except:
        # Trying list content and children variant
        attributes["content"] = children
        attributes["children"] = children
        instance = element_to_class(element.tag, attributes)

    return instance


def parse_layout(app, layout):
    tree = ElementTree.fromstring(layout)
    return parse_element(app, tree)
