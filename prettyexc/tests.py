
from prettyexc import PrettyException, Environment
from prettyexc.environment import default_python_environment, human_environment
from prettyexc import patch

def passert(test, *prints):
    try:
        assert(test)
    except AssertionError, e:
        for i, p in enumerate(prints):
            print i, ':', p
        print 'test:', test
        raise e

def test_default():
    e = PrettyException()
    assert(e)
    passert(str(e) == '', str(e))
    passert(repr(e) == '<prettyexc.core.PrettyException>', repr(e))
    assert(e._show_module() is True)
    passert(e._type(e.repr_environment) == 'prettyexc.core.PrettyException', e._type(e.repr_environment))
    assert(not e._message(e.unicode_environment))
    passert(str([e]) == '[<prettyexc.core.PrettyException>]', str([e]))

    e = PrettyException(200)
    passert(str(e) == '200', str(e))
    passert(str([e]) == '[<prettyexc.core.PrettyException(200)>]', str([e]))
    e = PrettyException("test")
    passert(str(e) == 'test', str(e))
    passert(str([e]) == '[<prettyexc.core.PrettyException("test")>]', str([e]))
    e = PrettyException(code=10)
    passert(str(e) == "code=10", str(e))
    passert(str([e]) == '[<prettyexc.core.PrettyException(code=10)>]', str([e]))
    e = PrettyException(mode='test')
    passert(str(e) == 'mode="test"')
    passert(str([e]) == '[<prettyexc.core.PrettyException(mode="test")>]', str([e]))

def test_pythonlike():
    p = Exception()
    e = PrettyException()
    assert(str(e) == str(p))
    p = Exception('message')
    e = PrettyException('message')
    assert(str(e) == str(p))
    p = Exception('many', 'args')
    e = PrettyException('many', 'args')
    #passert(str(e) == str(p), str(e), str(p))

def test_pythondefault():
    class PythonException(PrettyException):
        unicode_environment = default_python_environment
        repr_environment = default_python_environment

    e = PythonException()
    assert(e)
    assert(str(e) == 'PythonException')
    passert(str([e]) == '[PythonException]', str([e]))
    
def test_format():
    class T1Exception(PrettyException):
        message_format = u'Raise {code} with {description}.'

    e = T1Exception(code=200, description='OK')
    assert(e)
    passert(e.message == 'Raise 200 with OK.', e.message)
    passert(str(e) == 'Raise 200 with OK.', str(e))
    passert(repr(e) == '<T1Exception(code=200,description="OK")>', repr(e))

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
    passert(str(e) == 'T3Exception: Shows message.', str(e))

def test_env():
    custom_env = Environment(SHOW_MODULE=True, SHOW_ARGS=False)
    class T4Exception(PrettyException):
        unicode_environment = custom_env
    
    e = T4Exception(1, 2, 3, 'arg4')
    passert(str(e) == '__main__.T4Exception', str(e))

def test_patch():
    class AnException(Exception):
        def __init__(self, *args):
            super(AnException, self).__init__(*args)
            self.number = 10

        def value(self):
            return self.number + 2
    
    patch(AnException, PrettyException)
    e = AnException("message", user_id=1)
    passert(str(e) == '"message",user_id=1', str(e))
    passert(repr(e) == '<__main__.AnException("message",user_id=1)>', repr(e))
    passert(e.value() == 12)

    e = PrettyException()
    passert(str(e) == '', str(e))

if __name__ == '__main__':
    symbols = globals().keys()
    for k in symbols:
        if k.startswith('test_'):
            globals()[k]()
