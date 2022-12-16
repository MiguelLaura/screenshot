# =============================================================================
# Screenshot Utils
# =============================================================================
#
# Miscellaneous helper function used throughout the library.
#
import hashlib
from http.cookies import SimpleCookie


def md5(string):
    h = hashlib.md5()
    h.update(string.encode())
    return h.hexdigest()


def formatted_cookie(cookie, url):
    formatted_cookie = []

    parsed = SimpleCookie(cookie)

    for morsel in parsed.values():
        formatted_cookie.append({"name": morsel.key, "value": morsel.coded_value, "url": url})

    return formatted_cookie
