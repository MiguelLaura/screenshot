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

from screenshot.browser import BrowserContext
from screenshot.__version__ import __version__
from screenshot.cli.utils import LoadingBarWithError
from screenshot.exceptions import InvalidArgumentError
from screenshot.browser_authenticate import BrowserContextPersistent


def ckeck_args(cli_args):
    column = cli_args.column
    input_file = cli_args.file
    output_dir = cli_args.output_dir
    output = sys.stdout if not cli_args.output else open(cli_args.output, "w")
    authenticate_folder = cli_args.authenticate_folder
    cookies = cli_args.cookies
    throttle = cli_args.throttle

    if cookies and authenticate_folder:
        raise InvalidArgumentError(
            "'cookies' and 'authenticate_folder' can't be used together."
        )

    if authenticate_folder and not os.path.exists(authenticate_folder):
        raise InvalidArgumentError(
            "Could not find the '%s' browser folder."
            % authenticate_folder
        )

    if not input_file:
        input_file = CsvCellIO("url", cli_args.column)
        column = "url"

    if not isinstance(input_file, StringIO) and not os.path.exists(input_file):
        raise InvalidArgumentError(
            "Could not find the '%s' CSV file."
            % input_file
        )

    return column, input_file, output_dir, output, authenticate_folder, cookies, throttle


def take_command(cli_args):
    column, input_file, output_dir, output, authenticate_folder, cookies, throttle = ckeck_args(cli_args)

    enricher = casanova.enricher(input_file, output, add=["file_name", "error"])

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    loading_bar = LoadingBarWithError("Retrieving screenshots", unit="url")

    if authenticate_folder:
        with BrowserContextPersistent(authenticate_folder) as browser_screenshot:
            for row, url in enricher.cells(column, with_rows=True):

                try:
                    name_screenshot_file = browser_screenshot.screenshot_url(url, output_dir)
                    enricher.writerow(row, [name_screenshot_file, None])
                except (PlaywrightError, ValueError) as e:
                    loading_bar.update_errors()
                    loading_bar.print(e)
                    enricher.writerow(row, [None, e])

                loading_bar.update()
                time.sleep(throttle)

    else:
        with BrowserContext(cookies) as browser_screenshot:
            for row, url in enricher.cells(column, with_rows=True):

                try:
                    name_screenshot_file = browser_screenshot.screenshot_url(url, output_dir)
                    enricher.writerow(row, [name_screenshot_file, None])
                except (PlaywrightError, ValueError) as e:
                    loading_bar.update_errors()
                    loading_bar.print(e)
                    enricher.writerow(row, [None, e])

                loading_bar.update()
                time.sleep(throttle)
