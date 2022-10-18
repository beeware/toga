from .base import Widget


class WebView(Widget):
    def create(self):
        self._action('create WebView')

    def get_dom(self):
        self._action('get DOM')
        return 'DUMMY DOM'

    def set_on_key_down(self, handler):
        self._action('set on_key_down', handler=handler)

    def set_on_webview_load(self, handler):
        self._action('set on_webview_load', handler=handler)

    def set_content(self, root_url, content):
        self._action('set content', root_url=root_url, content=content)

    def set_user_agent(self, value):
        self._set_value('user_agent', value)

    def get_url(self):
        return self._get_value('url')

    def set_url(self, value):
        self._set_value('url', value)

    async def evaluate_javascript(self, javascript):
        self._action('evaluate_javascript', javascript=javascript)
        return 'JS RESULT'

    def invoke_javascript(self, javascript):
        self._action('invoke_javascript', javascript=javascript)
