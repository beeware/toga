import toga
from colosseum import CSS


class SwitchApp(toga.App):
    
    def startup(self):
        # Window class
        #   Main window of the application with title and size
        self.main_window = toga.MainWindow(self.name, size=(300, 150))
        self.main_window.app = self
        
        switch_style = CSS(padding=24)
        
        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[
                # Simple switch with label and callback function called toggled
                toga.Switch('Change Label', on_toggle=self.callbackLabel),

                # Switch with initial state
                toga.Switch('Initial state', is_on=True, style=CSS(margin_top=24)),
                
                # Switch with label and enable option
                toga.Switch('Disabled', enabled=False, style=CSS(margin_top=24))
            ],
            style=CSS(padding=24)
        )

        # Show the main window
        self.main_window.show()

    def callbackLabel(self, switch):
        # Some action when you hit the switch
        #   In this case the label will change
        switch.label = "switch is %s" % {0: "off", 1: "on"}[switch.is_on]
        

def main():
    # Application class
    #   App name and namespace
    app = SwitchApp('Switchs', 'org.pybee.helloworld')
    return app
