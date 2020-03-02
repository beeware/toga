import toga
from toga.style.pack import CENTER, COLUMN


class ImageViewApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)

        box = toga.Box()
        box.style.padding = 40
        box.style.update(alignment=CENTER)
        box.style.update(direction=COLUMN)

        # image from local path
        # load brutus.png from the package
        # We set the style width/height parameters for this one
        image_from_path = toga.Image('resources/brutus.png')
        imageview_from_path = toga.ImageView(image_from_path)
        imageview_from_path.style.update(height=72)
        imageview_from_path.style.update(width=72)
        box.add(imageview_from_path)

        # image from remote URL
        # no style parameters - we let Pack determine how to allocate
        # the space
        image_from_url = toga.Image('https://beeware.org/project/projects/libraries/toga/toga.png')
        imageview_from_url = toga.ImageView(image_from_url)
        box.add(imageview_from_url)

        self.main_window.content = box
        self.main_window.show()


def main():
    return ImageViewApp('ImageView', 'org.beeware.widgets.imageview')


if __name__ == '__main__':
    app = main()
    app.main_loop()
