import toga
from colosseum import CSS
from time import sleep

class ProgressBarApp(toga.App):
    
    def startup(self):
        # Main window of the application with title and size
        self.main_window = toga.MainWindow(self.name, size=(400, 400))
        self.main_window.app = self

        self.progress2 = toga.ProgressBar(value=0)
        
        # set up common styls
        label_style = CSS(flex=1, padding_right=24)
        box_style = CSS(flex_direction="row", padding=24)
        
        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[
                
                toga.Box(style=box_style, children=[
                    toga.Label("default ProgressBar", 
                        style=label_style),
                        
                    toga.ProgressBar(),
                ]),
                
                toga.Box(style=CSS(padding=24), children=[
                    toga.Label("Use the +/- buttons to change the progress",
                        style=label_style),
                    self.progress2,
                    toga.Box(
                        children=[
                            
                            toga.Button("+", on_press=self.increase_progress2,
                                style=CSS(margin=8, flex=1)),
                            toga.Button("-", on_press=self.decrease_progress2,
                                style=CSS(margin=8, flex=1)), 
                        ], 
                        style=CSS(flex=1, flex_direction="row")
                    ),
                    
                ]),
                
            ],
            style=CSS(padding=24)
        )

        self.main_window.show()
        
    def increase_progress2(self, button, **kw):
        self.progress2.value += 0.1 * self.progress2.max
    
    def decrease_progress2(self, button, **kw):
        self.progress2.value -= 0.1 * self.progress2.max
        

def main():
    # App name and namespace
    return ProgressBarApp('ProgressBar', 'org.pybee.examples.progressbar')
