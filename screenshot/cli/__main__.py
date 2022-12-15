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
#
import os
import csv
import sys
import ctypes
import casanova
from argparse import ArgumentParser
from playwright._impl._api_types import Error as PlaywrightError

from screenshot.browser import BrowserContext
from screenshot.__version__ import __version__
from screenshot.exceptions import InvalidArgumentsError
from screenshot.cli.constants import DEFAULT_PREBUFFER_BYTES


def main():

    # Building parser
    parser = ArgumentParser(prog="screenshot")

    parser.add_argument("--version", action="version", version="screenshot %s" % __version__)
    parser.add_argument("column", help="column where the urls are or a single url")
    parser.add_argument("--file", help="file where the urls are")
    parser.add_argument("output_dir", help="name of the directory where we should put the screenshots")
    parser.add_argument("--output", help="output file with the files' name")

    # Parsing arguments and triggering commands
    cli_args = parser.parse_args()

    column = cli_args.column
    input_file = cli_args.file
    output_dir = cli_args.output_dir
    output = sys.stdout if not cli_args.output else open(cli_args.output, "w")

    writer = csv.writer(output)

    if not column or not output_dir:
        parser.print_help()
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with BrowserContext() as browser_screenshot:

        if not input_file:
            name_screenshot_file = browser_screenshot.screenshot_url(column, output_dir)
            writer.writerow(["url", "file_name"])
            writer.writerow([column, name_screenshot_file])
            return

        if not os.path.exists(input_file):
            raise InvalidArgumentsError(
                'Could not find the "%s" CSV file.'
                % input_file
            )

        with open(input_file, "r") as f:
            reader = csv.DictReader(f)
            writer.writerow(reader.fieldnames + ["file_name"])

            for line in reader:
                url = line.get(column)

                if not url:
                    raise InvalidArgumentsError(
                        'Could not find the "%s" column containing the urls in the given CSV file.'
                        % column
                    )

                try:
                    name_screenshot_file = browser_screenshot.screenshot_url(url, output_dir)
                    writer.writerow([line[i] for i in reader.fieldnames] + [name_screenshot_file])
                except PlaywrightError as e:
                    if "Protocol error (Page.navigate): Cannot navigate to invalid URL" not in e.message:
                        raise e
                    print("Cannot navigate to url: %s" % url, file=sys.stderr)


if __name__ == "__main__":
    # Increasing max CSV file limit to avoid pesky issues
    csv.field_size_limit(int(ctypes.c_ulong(-1).value // 2))

    # Casanova global defaults
    casanova.set_default_prebuffer_bytes(DEFAULT_PREBUFFER_BYTES)
    casanova.set_default_ignore_null_bytes(True)

    main()
