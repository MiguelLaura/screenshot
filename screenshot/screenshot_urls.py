# =============================================================================
# Screenshot Screenshot_urls Function
# =============================================================================
#
# To add:
#   better error handling for args,
#   better error handling for urls
#

import os
import sys
import csv
from screenshot.utils import md5

from playwright.sync_api import sync_playwright
from screenshot.exceptions import InvalidArgumentsError
from playwright._impl._api_types import Error


def screenshot_urls(browser, url, output_dir):
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)
    page.wait_for_timeout(500)

    name = md5(url)

    page.screenshot(path=f"{output_dir}/{name}.png", full_page=True)

    context.close()

    return name


def open_browser(column, file, output_dir, output):
    with sync_playwright() as p:
        output = sys.stdout if not output else output

        browser = p.chromium.launch(channel="chrome")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output, "w") as f:
            writer = csv.writer(f)

            if not file:
                try:
                    name = screenshot_urls(browser, column, output_dir)
                    writer.writerow(["url", "file_name"])
                    writer.writerow([column, name])
                except Error as e:
                    print(e, file=sys.stderr)

            else:
                if not os.path.exists(file):
                    raise InvalidArgumentsError(
                        'Could not find the "%s" CSV file.'
                        % file
                    )

                with open(file, "r") as input_file:
                    reader = csv.DictReader(input_file)
                    writer.writerow(reader.fieldnames + ["file_name"])

                    for line in reader:

                        url = line.get(column)

                        if not url:
                            raise InvalidArgumentsError(
                                'Could not find the "%s" column containing the urls in the given CSV file.'
                                % column
                            )

                        try:
                            name = screenshot_urls(browser, url, output_dir)
                            writer.writerow([line[i] for i in reader.fieldnames] + [name])
                        except Error:
                            print("Cannot navigate to url: %s" % url, file=sys.stderr)

        browser.close()
