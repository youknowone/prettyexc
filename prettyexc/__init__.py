
"""
    pretty-exception
    ~~~~~~~~~~~~~~~~

    Common exception ancestor to print pretty exception to use instead of
    Exception.

    :copyright: (c) 2013 Jeong YunWon
    :license: 2-clause BSD.
"""

try:
    import pkg_resources
except ImportError:
    # pkg_resource is not available on Google App Engine
    VERSION = None
else:
    VERSION = pkg_resources.resource_string('prettyexc', 'version.txt').strip()  # noqa

from .environment import Environment
from .core import PrettyException
from .patch import patch

__all__ = 'Environment', 'PrettyException', 'patch'
