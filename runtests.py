import os
import sys

import django
from django.conf import settings
from django.core.management import call_command
from django.test.utils import get_runner


if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()
    call_command('makemigrations', 'paste')
    TestRunner = get_runner(settings)
    failures = TestRunner().run_tests(['tests'])
    sys.exit(bool(failures))
