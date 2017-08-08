from .base import Widget


class WebView(Widget):
    '''
    Web view widget
    '''
    def __init__(self, id=None, style=None, url=None, on_key_down=None, on_webview_load=None):
        '''
        Instantiate a new instance of the tree widget

        :param id:          An identifier for this widget.
        :type  id:          ``str``

        :param style:       an optional style object. If no style is provided then a
                            new one will be created for the widget.
        :type style:        :class:`colosseum.CSSNode`

        :param url: The URL to start with
        :type  url: ``str``

        :param on_key_down: The callback method for when the a key is pressed within
            the web view
        :type  on_key_down: ``callable``

        :param on_webview_load: The callback method for when the webview loads (or reloads)
        :type  on_webview_load: ``callable``
        '''
        super(WebView, self).__init__(id=id, style=style, url=url, on_key_down=on_key_down, on_webview_load=None)

    def _configure(self, url, on_key_down, on_webview_load=None):
        self.url = url
        self.on_key_down = on_key_down
        self.on_webview_load = on_webview_load

    @property
    def url(self):
        '''
        The current URL

        :rtype: ``str``
        '''
        return self._url

    @property
    def dom(self):
        '''
        The current DOM

        :rtype: ``str``
        '''
        return self._get_dom()

    @url.setter
    def url(self, value):
        self._url = value
        self._set_url(value)

    def set_content(self, root_url, content):
        '''
        Set the content of the web view

        :param root_url: The URL
        :type  root_url: ``str``

        :param content: The new content
        :type  content: ``str``
        '''
        self._url = root_url
        self._set_content(root_url, content)

    def _set_url(self, value):
        raise NotImplementedError('Webview widget must define _set_url()')

    def _get_dom(self, value):
        raise NotImplementedError('Webview widget must define _get_dom()')

    def _set_content(self, root_url, content):
        raise NotImplementedError('Webview widget must define _set_content()')

    def evaluate(self, javascript):
        '''
        Evaluate a JavaScript expression

        :param javascript: The javascript expression
        :type  javascript: ``str``
        '''
        raise NotImplementedError('Webview widget must define evaluate()')
