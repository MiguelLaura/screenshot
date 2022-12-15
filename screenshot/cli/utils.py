# =============================================================================
# Screenshot CLI Utils
# =============================================================================
#
# Miscellaneous helpers used by the CLI tools.
#
# Code from minet: https://github.com/medialab/minet/blob/master/minet/cli/utils.py
#
import sys
from tqdm import tqdm


def die(msg=None):
    if msg is not None:
        if not isinstance(msg, list):
            msg = [msg]

        for m in msg:
            print(m, file=sys.stderr)

    sys.exit(1)


class LoadingBar(tqdm):
    def __init__(
        self, desc, stats=None, unit=None, **kwargs
    ):

        if unit is not None:
            unit = " " + unit + "s"

        self.__stats = stats or {}

        if unit is not None:
            kwargs["unit"] = unit

        super().__init__(desc=desc, **kwargs)

    def print(self, *args, end="\n"):
        msg = " ".join(str(arg) for arg in args)
        self.write(msg, file=sys.stderr, end=end)

    def update_stats(self, **kwargs):
        for key, value in kwargs.items():
            self.__stats[key] = value

        return self.set_postfix(**self.__stats)

    def inc(self, name, amount=1):
        if name not in self.__stats:
            self.__stats[name] = 0

        self.__stats[name] += amount
        return self.update_stats()

    def update_errors(self):
        self.inc("errors")
        self.update_stats()
