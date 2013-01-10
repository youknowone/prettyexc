Pretty-Exception for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~

prettyexc provides common exception representation to make human-readable exception in easy way.

You can install the package from PyPI

    $ pip install prettyexc


Example
-------

    >>> from prettyexc import PrettyException

    >>> class SimpleException(PrettyException):
    ...     pass
    ... 
    >>> e = SimpleException('any', 'plain', 'args', code=200, description='OK')
    >>> print e
    SimpleException("any","plain","args",code=200,description="OK")
    >>> print [e, e]
    [<SimpleException("any","plain","args",code=200,description="OK")>, <SimpleException("any","plain","args",code=200,description="OK")>]

    >>> class MessageException(PrettyException):
    ...     message = u'You should select a user'
    ... 
    >>> e = MessageException(user_id=10)
    >>> print e
    MessageException(user_id=10): You should select a user
    >>> print [e, e]
    [<MessageException(user_id=10)>, <MessageException(user_id=10)>]

    >>> class FormatException(PrettyException):
    ...     message_format = u'User {user_id} has no permission.'
    ... 
    >>> e = FormatException(user_id=10)
    >>> print e
    FormatException(user_id=10): User 10 has no permission.
    >>> print e.message
    User 10 has no permission.
