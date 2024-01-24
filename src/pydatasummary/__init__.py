# Define pydatasummary version
from importlib_metadata import version as _v

# __version__ = "0.0.1"
__version__ = _v("pydatasummary")

del _v

# Import pydatasummary objects
from .ds import *  # noqa: F401, F403, E402
