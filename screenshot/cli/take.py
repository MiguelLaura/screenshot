# =============================================================================
# Screenshot Take CLI Action
# =============================================================================
#
# Logic of the `take` command.
#
import os
import sys
import time
import casanova
from io import StringIO
from casanova.utils import CsvCellIO
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from screenshot.browser import BrowserContext
from screenshot.__version__ import __version__
from screenshot.cli.reporters import report_error
from screenshot.cli.utils import LoadingBarWithError
from screenshot.cli.exceptions import InvalidArgumentError
from screenshot.browser_authenticate import BrowserContextPersistent


def ckeck_args(cli_args):
    column = cli_args.column
    input_file = cli_args.file
    directory = cli_args.directory
    output = sys.stdout if not cli_args.output else open(cli_args.output, "w")
    authenticate = cli_args.authenticate
    cookies = cli_args.cookies
    throttle = cli_args.throttle

    if cookies and authenticate:
        raise InvalidArgumentError(
            "'cookies' and 'authenticate' can't be used together."
        )

    if authenticate and not os.path.exists(authenticate):
        raise InvalidArgumentError(
            "Could not find the '%s' browser folder."
            % authenticate
        )

    if not input_file:
        input_file = CsvCellIO("url", cli_args.column)
        column = "url"

    if not isinstance(input_file, StringIO) and not os.path.exists(input_file):
        raise InvalidArgumentError(
            "Could not find the '%s' CSV file."
            % input_file
        )

    return column, input_file, directory, output, authenticate, cookies, throttle


def take_command(cli_args):
    column, input_file, directory, output, authenticate, cookies, throttle = ckeck_args(cli_args)

    enricher = casanova.enricher(input_file, output, add=["file_name", "error"])

    if not os.path.exists(directory):
        os.makedirs(directory)

    loading_bar = LoadingBarWithError("Retrieving screenshots", unit="url")

    browser_class = BrowserContext
    class_argument = cookies

    if authenticate:
        browser_class = BrowserContextPersistent
        class_argument = authenticate

    with browser_class(class_argument) as browser_screenshot:
        for row, url in enricher.cells(column, with_rows=True):

            try:
                name_screenshot_file = browser_screenshot.screenshot_url(url, directory)
                enricher.writerow(row, [name_screenshot_file, None])
            except (PlaywrightError, PlaywrightTimeoutError, ValueError) as e:
                loading_bar.update_errors()
                loading_bar.print("%s: %s" % (report_error(e), url))
                enricher.writerow(row, [None, report_error(e)])

            loading_bar.update()
            time.sleep(throttle)
