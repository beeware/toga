from toga import App, Box, Button, Label, ScrollContainer
from toga.style import Pack

def build(app):

    # wrapper that generates a visibility-toggler for the target widget
    def toggle_visibility_of(target):
        def handler(button):
            # widget is the button, target is what is being acted on
            if target.style.visibility == 'visible':
                target.style.visibility = 'hidden'
                button.label = button.label[0] + " (hidden)"  # label[0] is the button number
            else:
                target.style.visibility = 'visible'
                button.label = button.label[0]
        
        return handler

    root = Box(style=Pack(direction="column"))

    root.add(Label("This app tests the behavior of the visibility style property."))
    root.add(Label("Instructions: click each button (there are 8) and verify that the indicated label vanishes."))

    # CASE 1 - target is a single widget
    # ======
    root.add(Label("Case 1: target is a single widget"))
    case1_target = Label("Click button 1 to toggle my visibility")
    root.add(case1_target)
    root.add(Button("1", on_press=toggle_visibility_of(case1_target)))  


    # CASE 2 - target is a box that is a grandchild of the window
    # ======
    root.add(Label("Case 2: target is a box that is a grandchild of the window", style=Pack(padding_top=10)))
    case2_target = Box(children=[
        Label("Click button 2 to toggle my visibility"),
    ], style=Pack(direction="column"))
    root.add(case2_target)
    root.add(Button("2", on_press=toggle_visibility_of(case2_target)))


    # CASE 3 -  target is the direct child of the window
    # ======
    root.add(Label("Case 3: target is the direct child of the window", style=Pack(padding_top=10)))
    case3_target = root
    # root.add(case3_target)  # can't add root to itself!
    root.add(Label("Click button 3 to hide the root widget. You will have to restart this app"))
    root.add(Button("3", on_press=toggle_visibility_of(root)))


    # CASE 4 - target is a scroll container
    # ======
    root.add(Label("Case 4: target is a scroll container", style=Pack(padding_top=10)))
    case4_target = ScrollContainer(content=Label("Click button 4 to toggle my visibility"))
    root.add(case4_target)
    root.add(Button("4", on_press=toggle_visibility_of(case4_target)))


    # CASE 5 - target is a label that is a direct child of a scroll container
    # ======
    root.add(Label("Case 5: target is a label that is a direct child of a scroll container", style=Pack(padding_top=10)))
    case5_target = Label("Click button 5 to toggle my visibility")
    root.add(ScrollContainer(content=case5_target))
    root.add(Button("5", on_press=toggle_visibility_of(case5_target)))


    # CASE 6 - target is a box that is a direct child of a scroll container
    # ======
    root.add(Label("Case 6: target is a box that is a direct child of a scroll container", style=Pack(padding_top=10)))
    case6_target = Box(children=[Label("Click button 6 to toggle my visibility")])
    root.add(ScrollContainer(content=case6_target))
    root.add(Button("6", on_press=toggle_visibility_of(case6_target)))


    # CASE 7 - target is a box that is a grandchild of scroll container
    root.add(Label("Case 7: target is a box that is a grandchild of a scroll container", style=Pack(padding_top=10)))
    case7_target = Box(children=[Label("Click button 7 to toggle my visibility")])
    root.add(ScrollContainer(content=Box(children=[case7_target])))
    root.add(Button("7", on_press=toggle_visibility_of(case7_target)))

    # CASE 8 - target is a box that is a great grandchild of the window
    root.add(Label("Case 8: target is a box that is a great grandchild of the window", style=Pack(padding_top=10)))
    case8_target = Box(children=[Label("Click button 8 to toggle my visibility")])
    root.add(ScrollContainer(content=Box(children=[
        Box(children=[
            case8_target])])))
    root.add(Button("8", on_press=toggle_visibility_of(case8_target)))

    return root

def main():
    return App("Hide / Show Test", "org.beeware.hide_show", startup=build)