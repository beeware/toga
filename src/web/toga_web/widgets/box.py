from .base import Widget


class Box(Widget):
    def __html__(self):
        return """
            <div id="toga_{id}" class="toga box container" style="{style}">
            {content}
            </div>
        """.format(
            id=self.interface.id,
            content="\n".join(
                child._impl.__html__()
                for child in self.interface.children
            ),
            style=''
        )

    def create(self):
        pass

    def add_child(self, child):
        pass
