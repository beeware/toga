from .base import Widget


class WebView(Widget):
    def create(self):
        self._action('create WebView')

    def get_dom(self):
        self._action('get DOM')
        return 'DUMMY DOM'

    def set_content(self, root_url, content):
        self._action('set content', root_url=root_url, content=content)

    def set_user_agent(self, value):
        self._set_value('user_agent', value)

    def set_url(self, value):
        self._set_value('url', value)

    def evaluate(self, javascript):
        self._action('evaluate', javascript=javascript)
