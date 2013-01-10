
import sys

class Environment(object):
    """
    Environment uses 3-valued boolean-like configuration.
    True means turn on always.
    False means turn off always.
    None means automatic selection by value.
    """
    SHOW_CHEVRONS = False # None == False
    SHOW_MODULE = False # None: False if module starts with '__' else True
    SHOW_ARGS = True # None: False if no args else True
    SHOW_MESSAGE = False # None: False if no message else True

    STR_QUOTE = u'"'
    DEFAULT_CHARSET = sys.getdefaultencoding()

    def __init__(self, **kwargs):
        if self.DEFAULT_CHARSET == 'ascii':
            self.DEFAULT_CHARSET = 'utf-8'
        for kw, arg in kwargs.items():
            setattr(self, kw, arg)

default_python_environment = Environment()
default_unicode_environment = Environment(SHOW_MODULE=None, SHOW_ARGS=None, SHOW_MESSAGE=None)
default_repr_environment = Environment(SHOW_CHEVRONS=True, SHOW_MODULE=None, SHOW_ARGS=True)

human_environment = Environment(SHOW_ARGS=False, SHOW_MESSAGE=True)

