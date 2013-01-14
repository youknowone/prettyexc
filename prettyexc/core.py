
from .environment import default_unicode_environment, default_repr_environment, args_environment

def _arg_to_unicode(arg, env):
    if isinstance(arg, unicode):
        return u''.join((env.STR_QUOTE, arg, env.STR_QUOTE))
    elif isinstance(arg, str):
        return u''.join((env.STR_QUOTE, arg.decode(env.DEFAULT_CHARSET), env.STR_QUOTE))
    return unicode(arg)

def _kwarg_to_unicode(kw, arg, env):
    return u''.join((unicode(kw), u'=', _arg_to_unicode(arg, env)))


class PrettyException(Exception):
    message_format = None
    unicode_environment = default_unicode_environment
    repr_environment = default_repr_environment
    
    _req_args_count = 0
    _req_kwargs_keys = []
    
    @property
    def _args_kwargs_map(self):
        return self._req_kwargs_keys

    def __init__(self, *args, **kwargs):
        if self._args_kwargs_map:
            for i, key in enumerate(self._args_kwargs_map):
                if not key in kwargs:
                    try:
                        kwargs[key] = args[i]
                    except IndexError:
                        break # stop is no args anymore
            args = args[len(self._args_kwargs_map):]
        if self._req_args_count > len(args):
            raise InvalidArgumentCount(len(args), self._req_args_count)
        for key in self._req_kwargs_keys:
            if not key in kwargs:
                raise InvalidArgumentKeyword(key)
        self.args = args
        self.kwargs = kwargs
   
    def _show_module(self):
        """Override to modify 'auto' behavior.""" 
        return self.__class__.__module__[:2] != '__'

    def _type(self, env):
        """Override to modify type expresson."""
        if not env.SHOW_TYPE:
           return ''
        s = self.__class__.__name__
        mod = self.__class__.__module__
        show_module = env.SHOW_MODULE if env.SHOW_MODULE is not None else self._show_module()
        if show_module:
            s = '.'.join((mod, s))
        return s

    def _show_args(self, argss):
        """Override to modify 'auto' behavior."""
        return len(argss) > 0

    def _args(self, env):
        """Override to modify arguments expression."""
        if env.SHOW_ARGS is False:
            return ''
        if env.SHOW_ARGS is None and len(self.args) == 1 and not self.kwargs:
            return ''
        argss = [_arg_to_unicode(arg, env) for arg in self.args]
        argss += [_kwarg_to_unicode(kw, arg, env) for kw, arg in self.kwargs.items()]
        if env.SHOW_ARGS is not True and not self._show_args(argss):
            return ''
        return u','.join(argss)
  
    def _show_message(self, msg):
        """Override to modify 'auto' behavior."""
        return msg

    def _message(self, env):
        """Override to modify message expression."""
        if env.SHOW_MESSAGE == False:
            return ''
        msg = self.message
        if not self._show_message(msg):
            return ''
        return msg

    def format(self, env):
        """Top-level formatter. Override other methods to keep total form."""
        ss = []
        if env.SHOW_CHEVRONS:
            ss.append(u'<')
        typ = self._type(env)
        if typ:
            ss.append(typ)
            args = self._args(env)
            if args:
                ss.append(u'(')
                ss.append(args)
                ss.append(u')')
        msg = self._message(env)
        if typ and msg:
            ss.append(u': ')
        if msg:
            ss.append(msg)
        if env.SHOW_CHEVRONS:
            ss.append(u'>')
        return u''.join(ss)

    def __repr__(self):
        return self.format(self.repr_environment)

    def __unicode__(self):
        return self.format(self.unicode_environment)

    def __str__(self):
        return self.__unicode__().encode(self.unicode_environment.DEFAULT_CHARSET)

    def __getattr__(self, key):
        if key and key[0] != '_':
            try:
                return self.kwargs[key]
            except:
                pass
        sup = super(PrettyException, self)
        try:
            return sup.__getattr__()
        except:
            return sup.__getattribute__()

    @property
    def message(self):
        """Default message builder from message_format."""
        fmt = self.message_format
        if not fmt:
            # Python default Exception behavior
            if len(self.args) == 1 and not self.kwargs:
                return unicode(self.args[0])
            argss = list(self.args)
            for kw, arg in self.kwargs.items():
                argss.append('='.join((kw, unicode(arg))))
            if argss:
                return self._args(args_environment)
            return ''
        return fmt.format(*self.args, **self.kwargs)

class InvalidArgumentCount(PrettyException):
    message_format = u'At least {expected} arguments are expected but {given} arguments are given.'

    def __init__(self, given, expected):
        # override to avoid recursion
        self.args = []
        self.kwargs = {'given': given, 'expected': expected}

class InvalidArgumentKeyword(PrettyException):
    message_format = u'{expected} keyword are expected but not exists.'

    def __init__(self, expected):
        # override to avoid recursion
        self.args = []
        self.kwargs = {'expected': expected}

