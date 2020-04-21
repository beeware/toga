class Icon:
    SIZES = None
    EXTENSIONS = ['.png']
    path = ''

    def __init__(self, interface, **kwargs):
        interface.factory.not_implemented('Icon')
