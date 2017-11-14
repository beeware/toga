import toga
from colosseum import CSS


class SliderApp(toga.App):
    
    def startup(self):
        # Main window of the application with title and size
        self.main_window = toga.MainWindow(self.name, size=(640, 500))
        self.main_window.app = self
        
        # set up common styls
        label_style = CSS(flex=1, padding_right=24)
        box_style = CSS(flex_direction="row", padding=24)
        
        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[
                
                toga.Box(style=box_style, children=[
                    toga.Label("default Slider -- range is 0 to 1", 
                        style=label_style),
                        
                    toga.Slider(),
                ]),
                
                toga.Box(style=box_style, children=[
                    toga.Label("on a scale of 1 to 10, how easy is GUI with Toga?",
                        style=label_style),
                        
                    toga.Slider(range=(1, 10), default=10),
                ]),
                
                toga.Box(style=box_style, children=[
                    toga.Label("Sliders can be disabled", style=label_style),
                    
                    toga.Slider(enabled=False),
                ]),
                
                toga.Box(style=box_style, children=[
                    toga.Label("give a Slider some style!", style=label_style),
                    
                    toga.Slider(style=CSS(margin=16, width=300))
                ]),
                
                toga.Box(style=box_style, children=[
                    toga.Label("use the 'on_slide' callback to respond to changes", 
                        style=label_style),
                        
                    toga.Slider(on_slide=self.my_on_slide, range=(-40, 58)),
                ]),
            ],
            style=CSS(padding=24)
        )

        self.main_window.show()

    def my_on_slide(self, slider):
    
        # get the current value of the slider with `slider.value`
    
        print("The slider value changed to {0}".format(slider.value))
        

def main():
    # App name and namespace
    return SliderApp('Slider', 'org.pybee.examples.slider')
