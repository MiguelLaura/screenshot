# =============================================================================
# Screenshot Browser-authenticate
# =============================================================================
#
# Function to log the user to a browser from a browser folder (useful for Facebook, Twitter...)
#
from playwright.sync_api import sync_playwright

from screenshot.utils import md5


class BrowserContextPersistent(object):

    def __init__(self, authenticate_folder):
        self.browser = None
        self.playwright = None
        self.authenticate_folder = authenticate_folder

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch_persistent_context(self.authenticate_folder, channel="chrome", headless=False)
        return self

    def __exit__(self, exc_type, exc, tb):
        self.browser.close()
        self.playwright.stop()

    def screenshot_url(self, url, output_dir):
        page = self.browser.pages[0]
        page.goto(url)
        page.wait_for_timeout(500)

        name_screenshot_file = md5(url)

        page.screenshot(path="%s/%s.png" % (output_dir, name_screenshot_file), full_page=True)

        page.close()

        return name_screenshot_file
