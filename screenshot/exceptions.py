# =============================================================================
# Screenshot Custom CLI Exceptions
# =============================================================================
#
# Collection of handy custom exceptions.
#


class ScreenshotError(Exception):
    pass


class InvalidArgumentsError(ScreenshotError):
    pass
