

class Window:
    def __init__(self, id, title, content=None):
        self.id = id

        self.title = title
        self.set_content(content)

    def __html__(self):
        return """
            <nav id="toga:%s" data-toga-class="toga.Window" data-toga-ports="%s" class="navbar navbar-fixed-top navbar-dark bg-inverse">
                <a class="navbar-brand" href="#">%s</a>
                <ul class="nav navbar-nav">
                    <!--li class="nav-item active">
                      <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
                    </li-->
                </ul>
            </nav>""" % (
                self.id,
                '',  #  self.ports,
                self.title
            ) + self.content.__html__()

    def set_title(self, title):
        self.title = title
        dom.window.title = title

    def set_content(self, content):
        self.content = content
        if content:
            self.content.parent = self

    # HTML popups don't allow for titles, so we'll prepend it
    def info_dialog(self, title, message):
        dom.alert("%s\n\n%s" % (title, message));
