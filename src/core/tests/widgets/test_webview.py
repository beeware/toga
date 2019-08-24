import toga
import toga_dummy
from toga_dummy.utils import TestCase

from ..utils import async_test


class WebViewTests(TestCase):
    def setUp(self):
        super().setUp()

        self.url = 'https://beeware.org/'

        def callback(widget):
            pass

        self.on_key_down = callback
        self.web_view = toga.WebView(url=self.url,
                                     on_key_down=self.on_key_down,
                                     factory=toga_dummy.factory,
                                     user_agent='DUMMY AGENT')

    def test_widget_created(self):
        self.assertEqual(self.web_view._impl.interface, self.web_view)
        self.assertActionPerformed(self.web_view, 'create WebView')

    def test_setting_url_invokes_impl_method(self):
        new_url = 'https://github.com/'
        self.web_view.url = new_url
        self.assertEqual(self.web_view.url, new_url)
        self.assertValueSet(self.web_view, 'url', new_url)

    def test_set_content_invokes_impl_method(self):
        root_url = 'https://github.com/'
        new_content = """<!DOCTYPE html>
            <html>
              <body>
                <h1>My First Heading</h1>
                <p>My first paragraph.</p>
              </body>
            </html>
        """

        self.web_view.set_content(root_url, new_content)
        self.assertActionPerformedWith(self.web_view, 'set content', root_url=root_url, content=new_content)

    def test_get_dom(self):
        dom = self.web_view.dom
        self.assertEqual(dom, 'DUMMY DOM')
        self.assertActionPerformed(self.web_view, 'get DOM')

    def test_get_user_agent(self):
        self.assertEqual(self.web_view.user_agent, 'DUMMY AGENT')

    def test_set_user_agent(self):
        new_user_agent = 'DUMMY AGENT 2'
        self.web_view.user_agent = new_user_agent
        self.assertEqual(self.web_view.user_agent, new_user_agent)
        self.assertValueSet(self.web_view, 'user_agent', new_user_agent)

    @async_test
    async def test_evaluate_javascript(self):
        result = await self.web_view.evaluate_javascript('test(1);')
        self.assertActionPerformed(self.web_view, 'evaluate_javascript')
        self.assertEqual(result, 'JS RESULT')

    def test_invoke_javascript(self):
        self.web_view.invoke_javascript('test(1);')
        self.assertActionPerformed(self.web_view, 'invoke_javascript')
