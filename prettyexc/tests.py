
from prettyexc import PrettyException, Environment
from prettyexc import patch
from prettyexc.environment import default_python_environment, human_environment
from prettyexc.exceptions import InvalidArgumentCount, InvalidArgumentKeyword

def test_default():
    e = PrettyException()
    assert(e)
    assert(str(e) == '')
    assert(repr(e) == '<prettyexc.core.PrettyException>')
    assert(e._show_module() is True)
    assert(e._type(e.repr_environment) == 'prettyexc.core.PrettyException')
    assert(not e._message(e.unicode_environment))
    assert(str([e]) == '[<prettyexc.core.PrettyException>]')

    e = PrettyException(200)
    assert(str(e) == '200')
    assert(str([e]) == '[<prettyexc.core.PrettyException(200)>]')
    e = PrettyException("test")
    assert(str(e) == 'test')
    assert(str([e]) == '[<prettyexc.core.PrettyException("test")>]')
    e = PrettyException(code=10)
    assert(str(e) == "code=10")
    assert(str([e]) == '[<prettyexc.core.PrettyException(code=10)>]')
    e = PrettyException(mode='test')
    assert(str(e) == 'mode="test"')
    assert(str([e]) == '[<prettyexc.core.PrettyException(mode="test")>]')

def test_pythonlike():
    p = Exception()
    e = PrettyException()
    assert(str(e) == str(p))
    p = Exception('message')
    e = PrettyException('message')
    assert(str(e) == str(p))
    p = Exception('many', 'args')
    e = PrettyException('many', 'args')
    #assert(str(e) == str(p), str(e), str(p))

def test_pythondefault():
    class PythonException(PrettyException):
        unicode_environment = default_python_environment
        repr_environment = default_python_environment

    e = PythonException()
    assert(e)
    assert(str(e) == 'PythonException')
    assert(str([e]) == '[PythonException]')

def test_format():
    class T1Exception(PrettyException):
        message_format = u'Raise {code} with {description}.'

    e = T1Exception(code=200, description='OK')
    assert(e)
    assert(e.message == 'Raise 200 with OK.')
    assert(str(e) == 'Raise 200 with OK.')
    assert(repr(e) == '<T1Exception(code=200,description="OK")>')

def test_message():
    class T2Exception(PrettyException):
        message = u'You should see this message'

    e = T2Exception()
    assert(e)
    assert(str(e) == 'You should see this message')
    assert(repr(e) == '<T2Exception>')

def test_human():
    class T3Exception(PrettyException):
        unicode_environment = human_environment
        message = u'Shows message.'

    e = T3Exception()
    assert(str(e) == 'T3Exception: Shows message.')

def test_env():
    custom_env = Environment(SHOW_MODULE=True, SHOW_ARGS=False)
    class T4Exception(PrettyException):
        unicode_environment = custom_env

    e = T4Exception(1, 2, 3, 'arg4')
    assert(str(e) == '__main__.T4Exception')

def test_patch():
    class AnException(Exception):
        def __init__(self, *args):
            super(AnException, self).__init__(*args)
            self.number = 10

        def value(self):
            return self.number + 2

    patch(AnException, PrettyException)
    e = AnException("message", user_id=1)
    assert(str(e) == '"message",user_id=1')
    assert(repr(e) == '<__main__.AnException("message",user_id=1)>')
    assert(e.value() == 12)

    e = PrettyException()
    assert(str(e) == '')

def test_transition():
    class TransitionException(PrettyException):
        _args_kwargs_map = ['code', 'description']

    e = TransitionException(200, 'OK')
    assert(str(e) == 'code=200,description="OK"')

def test_constraint():
    class MinArgsException(PrettyException):
        _req_args_count = 2

    try:
        e = MinArgsException(0)
    except InvalidArgumentCount as e:
        assert e.expected == 2
        assert e.given == 1

    e = MinArgsException(0, 1)
    e = MinArgsException(0, 1, 2)

    class MinKwargsException(PrettyException):
        _req_kwargs_keys = ['code', 'desc']

    try:
        e = MinKwargsException(code=200)
    except InvalidArgumentKeyword as e:
        assert e.expected == 'desc'

    e = MinKwargsException(code=200, desc='blah')
    e = MinKwargsException(200, 'blah')
    assert e.code == 200
    assert e.desc == 'blah'


def test_get_with_index():
    class TestException(PrettyException):
        pass

    e = TestException(1, 2)
    assert e[0] == 1
    assert e[1] == 2


if __name__ == '__main__':
    symbols = list(globals().keys())
    for k in symbols:
        if k.startswith('test_'):
            globals()[k]()
