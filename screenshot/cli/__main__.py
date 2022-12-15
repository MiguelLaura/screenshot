#!/usr/bin/env python
# =============================================================================
# Screenshot CLI Endpoint
# =============================================================================
#
# CLI enpoint of the Screenshot library.
#
# To add:
#   better error handling for args,
#   better error handling for urls
#   add --cookie (?)
#
import os
import csv
import sys
import ctypes
import casanova
from io import StringIO
from casanova.utils import CsvCellIO
from argparse import ArgumentParser
from playwright.sync_api import Error as PlaywrightError

from screenshot.cli.utils import LoadingBar
from screenshot.browser import BrowserContext
from screenshot.__version__ import __version__
from screenshot.exceptions import InvalidArgumentError
from screenshot.cli.constants import DEFAULT_PREBUFFER_BYTES


def ckeck_args(cli_args):
    column = cli_args.column
    input_file = cli_args.file
    output_dir = cli_args.output_dir
    output = sys.stdout if not cli_args.output else open(cli_args.output, "w")

    if not column or not output_dir:
        return None * 4

    if not input_file:
        input_file = CsvCellIO("url", cli_args.column)
        column = "url"

    if not isinstance(input_file, StringIO) and not os.path.exists(input_file):
        raise InvalidArgumentError(
            'Could not find the "%s" CSV file.'
            % input_file
        )

    return column, input_file, output_dir, output


def main():

    # Building parser
    parser = ArgumentParser(prog="screenshot")

    parser.add_argument("column", help="column where the urls are or a single url")
    parser.add_argument("file", nargs="?", default=None, help="file where the urls are")
    parser.add_argument("output_dir", help="name of the directory where we should put the screenshots")
    parser.add_argument("--output", help="output file with the files' name")
    parser.add_argument("--version", action="version", version="screenshot %s" % __version__)

    # Parsing arguments and triggering commands
    cli_args = parser.parse_args()

    column, input_file, output_dir, output = ckeck_args(cli_args)

    if not column:
        parser.print_help()

    enricher = casanova.enricher(input_file, output, add=["file_name"])

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    loading_bar = LoadingBar("Retrieving screenshots", unit="url")

    with BrowserContext() as browser_screenshot:

        for row, url in enricher.cells(column, with_rows=True):
            loading_bar.update()

            try:
                name_screenshot_file = browser_screenshot.screenshot_url(url, output_dir)
                enricher.writerow(row, [name_screenshot_file])
            except PlaywrightError as e:
                loading_bar.update_errors()
                if "Protocol error (Page.navigate): Cannot navigate to invalid URL" not in e.message:
                    raise e
                loading_bar.print("Cannot navigate to URL: %s" % url)


if __name__ == "__main__":
    # Increasing max CSV file limit to avoid pesky issues
    csv.field_size_limit(int(ctypes.c_ulong(-1).value // 2))

    # Casanova global defaults
    casanova.set_default_prebuffer_bytes(DEFAULT_PREBUFFER_BYTES)
    casanova.set_default_ignore_null_bytes(True)

    main()
