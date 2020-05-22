from toga import App, Box, Label, ScrollContainer, Switch
from toga.style import Pack


def build(app):

    # wrapper that generates a visibility-toggler for the target widget
    def toggle_visibility_of(target):
        def handler(switch):
            # widget is the button, target is what is being acted on
            if switch.is_on:
                target.style.visibility = 'visible'
            else:
                target.style.visibility = 'hidden'

        return handler

    root = Box(id="root", style=Pack(direction="column"))

    root.add(Label("This app tests the behavior of the visibility style \
        property."))
    root.add(Label("Instructions: click each button (there are 8) and verify \
        that the indicated label vanishes."))

    # CASE 1 - target is a single widget
    # ======
    case1_target = Label("Click switch 1 to toggle my visibility")
    root.add(Switch(
        label="Case 1: target is a single widget",
        is_on=True,
        style=Pack(flex=1),
        on_toggle=toggle_visibility_of(case1_target)))
    root.add(case1_target)

    # CASE 2 - target is a box that is a grandchild of the window
    # ======
    case2_target = Box(children=[
        Label("Click switch 2 to toggle my visibility"),
    ], style=Pack(direction="column"))
    root.add(Switch(
        label="Case 2: target is a box that is a grandchild of the window",
        is_on=True,
        style=Pack(flex=1),
        on_toggle=toggle_visibility_of(case2_target)))
    root.add(case2_target)

    # CASE 8 - target is a box that is a great grandchild of the window
    # ======
    case8_target = Box(children=[
        Label("Click switch 8 to toggle my visibility")])
    root.add(Switch(
        "Case 8: target is a box that is a great grandchild of the window",
        is_on=True,
        style=Pack(flex=1),
        on_toggle=toggle_visibility_of(case8_target)))
    root.add(ScrollContainer(
        content=Box(children=[
            Box(children=[
                case8_target])])))

    # CASE 4 - target is a scroll container
    # ======
    case4_target = ScrollContainer(
        content=Label("Click switch 4 to toggle my visibility"))
    root.add(Switch(
        label="Case 4: target is a scroll container",
        is_on=True,
        style=Pack(flex=1),
        on_toggle=toggle_visibility_of(case4_target)))
    root.add(case4_target)

    # CASE 5 - target is a label that is a direct child of a scroll container
    # ======
    case5_target = Label("Click switch 5 to toggle my visibility")
    root.add(Switch(
        label="Case 5: target is a label that is a direct child of a scroll \
            container",
        is_on=True,
        style=Pack(flex=1),
        on_toggle=toggle_visibility_of(case5_target)))
    root.add(ScrollContainer(content=case5_target))

    # CASE 6 - target is a box that is a direct child of a scroll container
    # ======
    case6_target = Box(children=[
        Label("Click switch 6 to toggle my visibility")])
    root.add(Switch(
        label="Case 6: target is a box that is a direct child of a scroll \
            container",
        is_on=True,
        style=Pack(flex=1),
        on_toggle=toggle_visibility_of(case6_target)))
    root.add(ScrollContainer(content=case6_target))

    # CASE 7 - target is a box that is a grandchild of scroll container
    case7_target = Box(children=[
        Label("Click switch 7 to toggle my visibility")])
    root.add(Switch(
        label="Case 7: target is a box that is a grandchild of a scroll \
            container",
        is_on=True,
        style=Pack(flex=1),
        on_toggle=toggle_visibility_of(case7_target)))
    root.add(ScrollContainer(content=Box(children=[case7_target])))

    # CASE 9 - target is a box with a hidden label and a visible label
    case9_target = Box(
        id="case9_target",
        style=Pack(direction="column"),
        children=[
            Label(
                id="case9_hidden_label",
                text="I should always be invisible! If you see me, this test \
                    failed",
                style=Pack(visibility="hidden")),
            Label("Click switch 9 to toggle my visibility")])
    root.add(Switch(
        label="Case 9: target is a box with a hidden label and visible label",
        is_on=True,
        style=Pack(flex=1),
        on_toggle=toggle_visibility_of(case9_target)))
    root.add(case9_target)

    # CASE 10 - initially hidden container content
    root.add(ScrollContainer(
        content=Label(
            text="I should always be invisible! If you see me, this test \
                failed",
            style=Pack(visibility="hidden"))))

    # CASE 3 - target is the direct child of the window
    # ======
    case3_target = root
    root.add(Switch(
        label="Case 3: target is the direct child of the window",
        is_on=True,
        style=Pack(flex=1),
        on_toggle=toggle_visibility_of(case3_target)))
    # root.add(case3_target)  # can't add root to itself!
    root.add(Label("Click switch 3 to hide the root widget. You will have to \
        restart this app"))

    return root


def main():
    return App("Hide / Show Test", "org.beeware.hide_show", startup=build)
