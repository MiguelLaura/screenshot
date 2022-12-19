# =============================================================================
# Screenshot CLI Reporters
# =============================================================================
#
# Various reporters whose goal is to convert errors etc. into human-actionable
# labels in CSV format, for instance.
#
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


def playwright_error_reporter(error):
    msg = repr(error).lower()

    if "cannot navigate to invalid url" in msg:
        return "invalid-URL"

    if "err_internet_disconnected" in msg:
        return "internet-disconnected"

    return "playwright-error"


def request_error_reporter(error):
    msg = repr(error).lower()

    if "unknown url type" in msg:
        return "invalid-URL"

    return "request-error"


ERROR_REPORTERS = {
    PlaywrightError: playwright_error_reporter,
    PlaywrightTimeoutError: "timeout-error",
    ValueError: request_error_reporter,
}


def report_error(error):
    reporter = ERROR_REPORTERS.get(type(error), repr)

    return reporter(error) if callable(reporter) else reporter
