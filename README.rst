Pretty-Exception for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~

prettyexc provides common exception representation to make human-readable exception in easy way.

You can install the package from PyPI

    $ pip install prettyexc


Example
-------

    >>> from prettyexc import PrettyException

Put and get your arguments always

    >>> class SimpleException(PrettyException):
    ...     pass
    ... 
    >>> e = SimpleException('any', 'plain', 'args', code=200, description='OK')
    >>> raise e
    
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    __main__.SimpleException: "any","plain","args",code=200,description="OK"
    SimpleException("any","plain","args",code=200,description="OK")

    >>> print [e, e]
    [<SimpleException("any","plain","args",code=200,description="OK")>, <SimpleException("any","plain","args",code=200,description="OK")>]

Set default message

    >>> class MessageException(PrettyException):
    ...     message = u'You should select a user'
    ... 
    >>> e = MessageException(user_id=10)
    >>> raise e
    
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    __main__.MessageException: You should select a user
    
    >>> print [e, e]
    [<MessageException(user_id=10)>, <MessageException(user_id=10)>]

Set message formatter

    >>> class FormatException(PrettyException):
    ...     message_format = u'User {user_id} has no permission.'
    ... 
    >>> e = FormatException(user_id=10)
    >>> raise e
    
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    __main__.FormatException: User 10 has no permission.
    
    >>> print e.message
    User 10 has no permission.

Patch existing exceptions

    >>> from prettyexc import patch
    >>> class AnException(Exception): pass
    ... 
    >>> patch(AnException, PrettyException)
    >>> raise AnException(status=404)

    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    __main__.AnException: status=404
