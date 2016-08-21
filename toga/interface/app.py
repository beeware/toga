class App(object):
    '''Toga App

    The App is the top level of any GUI program. It is the manager of all the
    other bits of the GUI app: the main window and events that window generates
    like user input.

    When you create an App you need to provide it a name, an id for uniqueness
    (by convention, the identifier is a "reversed domain name".) and an
    optional startup function which should run once the App has initialised.
    The startup function typically constructs some initial user interface.

    Once the app is created you should invoke the main_loop() method, which
    will hand over execution of your program to Toga to make the App interface
    do its thing.

    Here is the absolute minimum App::

        app = toga.App('Empty App', 'org.pybee.empty')
        app.main_loop()
    '''
    def __init__(self, name, app_id, icon=None, startup=None):
        raise NotImplemented

    def main_loop(self):
        '''Invoke the application to handle user input.

        This method typically only returns once the application is exiting.
        '''
        raise NotImplemented
