# =============================================================================
# Screenshot Browser Class
# =============================================================================
#
# Class to instantiate browser, use it and properly close it
#
import browser_cookie3
from playwright_stealth import stealth_sync
from playwright.sync_api import sync_playwright

from screenshot.utils import md5


class BrowserContext(object):

    def __init__(self, cookies):
        self.browser = None
        self.playwright = None
        self.cookies = cookies

    def __enter__(self):
        self.playwright = sync_playwright().start()
        if self.cookies:
            self.cookies = []
            jar = getattr(browser_cookie3, "chrome")()
            for cookie in jar:
                self.cookies.append(
                    {
                        "domain": cookie.domain,
                        "name": cookie.name,
                        "value": cookie.value,
                        "path": cookie.path,
                        "secure": True if cookie.secure else False,
                        "expires": cookie.expires,
                        "is_expired": True if cookie.is_expired else False,
                    }
                )
        self.browser = self.playwright.chromium.launch(channel="chrome")
        return self

    def __exit__(self, exc_type, exc, tb):
        self.browser.close()
        self.playwright.stop()

    def screenshot_url(self, url, directory):
        context = self.browser.new_context()

        if self.cookies:
            context.add_cookies(self.cookies)

        page = context.new_page()
        stealth_sync(page)
        page.goto(url)
        page.wait_for_timeout(3000)

        name_screenshot_file = md5(url)

        page.screenshot(path="%s/%s.png" % (directory, name_screenshot_file), full_page=True)

        page.close()
        context.close()

        return name_screenshot_file
