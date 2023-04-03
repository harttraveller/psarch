from pathlib import Path

HOME = Path.home()
FILES = HOME / ".psarch"


# TODO: add windows support
# TODO: add linux support
SUPPORTED_DEVICES = {"Darwin": {"arm", "i386"}}
