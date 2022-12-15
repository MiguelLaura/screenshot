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
        with sync_playwright() as p:
            self.browser = p.chromium.launch(channel="chrome")

    def __enter__(self):
        return self

    def __exit__(self):
        self.browser.close()

    def screenshot_url(self, url, output_dir):
        context = self.browser.new_context()

        page = context.new_page()
        page.goto(url)
        page.wait_for_timeout(500)

        name_screenshot_file = md5(url)

        page.screenshot(path="%s/%s.png" % (output_dir, name_screenshot_file), full_page=True)

        context.close()

        return name_screenshot_file
