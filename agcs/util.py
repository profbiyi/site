import sys
from ast import literal_eval


def run_with_args(func, args=None):
    """Parse arguments from ``sys.argv`` or given list of *args* and pass
    them to *func*.
    If ``--help`` is passed to program, print usage information.
    """
    args, kwargs = parse_args(args)
    if kwargs.get('help'):
        from inspect import getargspec
        argspec = getargspec(func)
        if argspec.defaults:
            defaults_count = len(argspec.defaults)
            args = argspec.args[:-defaults_count]
            defaults = zip(argspec.args[-defaults_count:], argspec.defaults)
        else:
            args = argspec.args
            defaults = []
        usage = 'usage: %s [--help]' % sys.argv[0]
        if args:
            usage += ' ' + ' '.join(args)
        if defaults:
            usage += ' ' + ' '.join(('[%s=%r]' % pair for pair in defaults))
        if argspec.varargs:
            usage += ' ' + '*' + argspec.varargs
        if argspec.keywords:
            usage += ' ' + '**' + argspec.keywords
        print(usage)
    else:
        return func(*args, **kwargs)


def parse_args(args=None):
    """Parse positional and keyword arguments from ``sys.argv`` or given list
    of *args*.
    :param args: list of string to parse, defaults to ``sys.argv[1:]``.
    :return: :class:`tuple` of positional args and :class:`dict` of keyword
        arguments.
    Positional arguments have no specific syntax. Keyword arguments must be
    written as ``--{keyword-name}={value}``::
        >>> parse_args(['1', 'hello', 'True', '3.1415926', '--force=True'])
        ((1, 'hello', True, 3.1415926), {'force': True})
    """
    if args is None:
        args = sys.argv[1:]

    positional_args, kwargs = (), {}
    for arg in args:
        if arg.startswith('--'):
            arg = arg[2:]
            try:
                key, raw_value = arg.split('=', 1)
                value = parse_literal(raw_value)
            except ValueError:
                key = arg
                value = True
            kwargs[key.replace('-', '_')] = value
        else:
            positional_args += (parse_literal(arg),)

    return positional_args, kwargs


def parse_literal(string):
    """Parse Python literal or return *string* in case :func:`ast.literal_eval`
    fails."""
    try:
        return literal_eval(string)
    except (ValueError, SyntaxError):
        return string
