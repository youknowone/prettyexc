
from .core import PrettyException


def patch(Exc, Template=PrettyException):
    # functions
    def __init__(self, *args, **kwargs):
        self.__original_init__(*args)
        self._delegate = Template(*args, **kwargs)
        self._delegate._type = lambda env: '' if not env.SHOW_TYPE else '.'.join((self.__class__.__module__, self.__class__.__name__)) if env.SHOW_MODULE is None or env.SHOW_MODULE else self.__class__.__name__

    def __repr__(self):
        return self._delegate.__repr__()

    def __unicode__(self):
        return self._delegate.__unicode__()

    def __str__(self):
        return self._delegate.__str__()

    # properties
    def args(self):
        return self._delegate.args

    def kwargs(self):
        return self._delegate.kwargs

    def message(self):
        return self._delegate.message

    funcs = {'__init__': __init__, '__repr__': __repr__, '__unicode__': __unicode__, '__str__': __str__}
    props = {'args': args, 'kwargs': kwargs, 'message': message}

    Exc.__original_init__ = Exc.__init__
    for name, func in funcs.items():
        setattr(Exc, name, func)
    for name, func in props.items():
        setattr(Exc, name, property(func))
