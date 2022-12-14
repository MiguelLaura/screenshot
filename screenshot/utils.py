# =============================================================================
# Screenshot Utils
# =============================================================================
#
# Miscellaneous helper function used throughout the library.
#
import hashlib


def md5(string):
    h = hashlib.md5()
    h.update(string.encode())
    return h.hexdigest()
