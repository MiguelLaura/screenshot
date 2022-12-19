# =============================================================================
# Screenshot Browser Class
# =============================================================================
#
# Class to instantiate browser, use it and properly close it
#
import browser_cookie3
from minet.web import CookieResolver
from playwright_stealth import stealth_sync
from playwright.sync_api import sync_playwright

from screenshot.utils import md5, formatted_cookie


class BrowserContext(object):

    def __init__(self, cookies):
        self.browser = None
        self.playwright = None
        self.cookies = cookies

    def __enter__(self):
        self.playwright = sync_playwright().start()
        if self.cookies:
            self.cookies = CookieResolver(browser_cookie3.chrome())
        self.browser = self.playwright.chromium.launch(channel="chrome")
        return self

    def __exit__(self, exc_type, exc, tb):
        self.browser.close()
        self.playwright.stop()

    def screenshot_url(self, url, output_dir):
        context = self.browser.new_context()

        if self.cookies:
            cookie = self.cookies(url)
            playwright_cookie = formatted_cookie(cookie, url)
            context.add_cookies(playwright_cookie)

        page = context.new_page()
        stealth_sync(page)
        page.goto(url)
        page.wait_for_timeout(3000)

        name_screenshot_file = md5(url)

        page.screenshot(path="%s/%s.png" % (output_dir, name_screenshot_file), full_page=True)

        page.close()
        context.close()

        return name_screenshot_file
