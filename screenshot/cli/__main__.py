#!/usr/bin/env python
# =============================================================================
# Screenshot CLI Endpoint
# =============================================================================
#
# CLI enpoint of the Screenshot library.
#
# To add:
#   better error handling for urls
#   add column in output file with errors
#   resume option
#
import sys
import csv
import ctypes
import casanova
from argparse import ArgumentParser

from screenshot.__version__ import __version__
from screenshot.cli.constants import DEFAULT_PREBUFFER_BYTES


def main():

    # Building parser
    parser = ArgumentParser(prog="screenshot")
    parser.add_argument("--version", action="version", version="screenshot %s" % __version__)

    subparsers = parser.add_subparsers(dest="command")

    authenticate = subparsers.add_parser("authenticate", help="authenticate in a browser and save browser info in a authenticate_folder")
    authenticate.add_argument("folder", help="folder name where the browser info must be saved")

    take = subparsers.add_parser("take", help="Take screenshot")
    take.add_argument("column", help="column where the urls are or a single url")
    take.add_argument("file", nargs="?", default=None, help="file where the urls are.  Defaults to None.")
    take.add_argument("output_dir", help="name of the directory where we should put the screenshots")
    take.add_argument("--output", "-o", help="output file with the files name")
    take.add_argument("--authenticate_folder", "-a", default=None, help="authenticate_folder where the browser info are (useful for Facebook, Twitter...). Not compatible with 'cookie'")
    take.add_argument("--cookies", "-c", action="store_true", help="get cookies from chrome (won't work for Facebook, Twitter). Not compatible with 'authenticate_folder'")
    take.add_argument("--throttle", "-t", default=0, type=int, help="time to wait between accessing to an other URL. Defaults to 0")

    cli_args = parser.parse_args()

    if cli_args.command == "authenticate":
        from screenshot.cli.authenticate import authenticate_command
        authenticate_command(cli_args)

    elif cli_args.command == "take":
        from screenshot.cli.take import take_command
        take_command(cli_args)

    else:
        parser.print_help(file=sys.stderr)


if __name__ == "__main__":
    # Increasing max CSV file limit to avoid pesky issues
    csv.field_size_limit(int(ctypes.c_ulong(-1).value // 2))

    # Casanova global defaults
    casanova.set_default_prebuffer_bytes(DEFAULT_PREBUFFER_BYTES)
    casanova.set_default_ignore_null_bytes(True)

    main()
