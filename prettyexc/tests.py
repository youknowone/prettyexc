
from prettyexc import PrettyException
from prettyexc.environment import Environment
from prettyexc.environment import default_python_environment, human_environment


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
    passert(str(e) == 'prettyexc.PrettyException', str(e))
    assert(e._show_module() is True)
    assert(e._type(e.unicode_environment) == 'prettyexc.PrettyException')
    assert(not e._message(e.unicode_environment))
    passert(str([e]) == '[<prettyexc.PrettyException>]', str([e]))

    e = PrettyException(200)
    assert(str(e) == 'prettyexc.PrettyException(200)')
    passert(str([e]) == '[<prettyexc.PrettyException(200)>]', str([e]))
    e = PrettyException("test")
    assert(str(e) == 'prettyexc.PrettyException("test")')
    passert(str([e]) == '[<prettyexc.PrettyException("test")>]', str([e]))
    e = PrettyException(code=10)
    assert(str(e) == 'prettyexc.PrettyException(code=10)')
    passert(str([e]) == '[<prettyexc.PrettyException(code=10)>]', str([e]))
    e = PrettyException(mode='test')
    assert(str(e) == 'prettyexc.PrettyException(mode="test")')
    passert(str([e]) == '[<prettyexc.PrettyException(mode="test")>]', str([e]))

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
    passert(str(e) == 'T1Exception(code=200,description="OK"): Raise 200 with OK.', str(e))
    passert(e.__repr__() == '<T1Exception(code=200,description="OK")>', e.__repr__())

def test_message():
    class T2Exception(PrettyException):
        message = u'You should see this message'

    e = T2Exception()
    assert(e)
    assert(str(e) == 'T2Exception: You should see this message')

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


if __name__ == '__main__':
    symbols = globals().keys()
    for k in symbols:
        if k.startswith('test_'):
            globals()[k]()
