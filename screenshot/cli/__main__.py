#!/usr/bin/env python
# =============================================================================
# Screenshot CLI Endpoint
# =============================================================================
#
# CLI enpoint of the Screenshot library.
#
import csv
import sys
import ctypes
import casanova
from tqdm import tqdm
from argparse import ArgumentParser

from screenshot.screenshot_urls import open_browser
from screenshot.__version__ import __version__
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
    file = cli_args.file
    output_dir = cli_args.output_dir
    output = cli_args.output

    if not column or not output_dir:
        parser.print_help()

    else:
        open_browser(column, file, output_dir, output)


if __name__ == "__main__":
    # Increasing max CSV file limit to avoid pesky issues
    csv.field_size_limit(int(ctypes.c_ulong(-1).value // 2))

    # Casanova global defaults
    casanova.set_default_prebuffer_bytes(DEFAULT_PREBUFFER_BYTES)
    casanova.set_default_ignore_null_bytes(True)

    main()
