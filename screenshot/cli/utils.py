# =============================================================================
# Screenshot CLI Utils
# =============================================================================
#
# Miscellaneous helpers used by the CLI tools.
#
import sys
from minet.cli.utils import LoadingBar


def die(msg=None):
    if msg is not None:
        if not isinstance(msg, list):
            msg = [msg]

        for m in msg:
            print(m, file=sys.stderr)

    sys.exit(1)


class LoadingBarWithError(LoadingBar):

    def update_errors(self):
        self.inc("errors")
