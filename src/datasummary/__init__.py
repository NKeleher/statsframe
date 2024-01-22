# Define datasummary version
from importlib_metadata import version as _v

# __version__ = "0.0.1"
__version__ = _v("datasummary")

del _v

# Import datasummary objects
from .ds import *  # noqa: F401, F403, E402
