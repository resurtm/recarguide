import platform
import sys

import django
from django.conf import settings


def strings(request):
    version = sys.version.split('\n')

    return {
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE['PUBLISHABLE_KEY'],

        'DJANGO_VERSION': django.get_version().strip(),
        'PYTHON_VERSION1': version[0].strip(),
        'PYTHON_VERSION2': version[1].strip(),
        'PLATFORM': platform.platform().strip(),
        'PLATFORM_VERSION': platform.version().strip(),
    }
