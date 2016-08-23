#!/usr/bin/env python
import os, sys
import django
from django.conf import settings
from django.test.utils import get_runner
from agcs import util

if __name__ == "__main__":
    from tests import __all__ as modules

    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()

    args, opts = util.parse_args(sys.argv[1:])

    TestRunner = get_runner(settings)
    test_runner = TestRunner(**opts)

    failures = test_runner.run_tests(
        args and list(
            'tests.'+ a for a in args
        ) or ['tests.'+ m for m in modules]
    )

    sys.exit(bool(failures))
