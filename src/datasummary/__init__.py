# Define datasummary version
from importlib_metadata import version as _v

# __version__ = "0.1.0"
__version__ = _v("great_tables")

del _v

# Import datasummary objects
from .ds import *  # noqa: F401, F403, E402
