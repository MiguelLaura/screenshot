# =============================================================================
# Screenshot Authenticate CLI Action
# =============================================================================
#
# Logic of the `authenticate` command.
#
import time
from playwright.sync_api import sync_playwright


def authenticate_command(cli_args):

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(cli_args.folder, channel="chrome", headless=False)
        # Execute login steps manually in the browser window
        browser.wait_for_event("close", timeout=0)
        # Need time to get closed properly
        time.sleep(1)
