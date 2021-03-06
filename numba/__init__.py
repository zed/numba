import sys
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="\n\033[1m%(levelname)s -- %(module)s:%(lineno)d:%(funcName)s\033[0m\n%(message)s")

try:
    from . import minivect
except ImportError:
    print logging.error("Did you forget to update submodule minivect?")
    print logging.error("Run 'git submodule init' followed by 'git submodule update'")
    raise

from . import _numba_types
from ._numba_types import *
from . import decorators
from .decorators import *

def test():
    from subprocess import check_call

    check_call([sys.executable, '-m', 'numba.tests.test_all'])


__all__ = _numba_types.__all__ + decorators.__all__
