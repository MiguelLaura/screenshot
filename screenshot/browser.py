# =============================================================================
# Screenshot Browser Class
# =============================================================================
#
# Class to instantiate browser, use it and properly close it
#
from playwright.sync_api import sync_playwright

from screenshot.utils import md5


class BrowserContext(object):

    def __init__(self):
        self.browser = None
        self.playwright = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(channel="chrome")
        return self

    def __exit__(self, exc_type, exc, tb):
        self.browser.close()
        self.playwright.stop()

    def screenshot_url(self, url, output_dir):
        context = self.browser.new_context()

        page = context.new_page()
        page.goto(url)
        page.wait_for_timeout(500)

        name_screenshot_file = md5(url)

        page.screenshot(path="%s/%s.png" % (output_dir, name_screenshot_file), full_page=True)

        page.close()
        context.close()

        return name_screenshot_file
