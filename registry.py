import os
from django.conf import settings
from django.core import management
from django.conf.urls import url
from django.http import HttpResponse
from distutils.util import strtobool

__version__ = 0.1

DEBUG = strtobool(os.getenv('DEBUG', 'True'))
ROOT_URLCONF = 'registry'
DATABASES = {'default': {}}  # required regardless of actual usage
SECRET_KEY = os.getenv('SECRET_KEY', 'Please set a SECRET_KEY as an env var.')

if not settings.configured:
    settings.configure(**locals())


def csw(request, catalog=None):
    """CSW dispatch view"""
    return HttpResponse('{catalog}'.format(catalog=(catalog or 'default')))


urlpatterns = [
    url(r'^$', csw),
    url(r'^(?P<catalog>\w+)?$', csw),
]


if __name__ == '__main__':  # pragma: no cover
    management.execute_from_command_line()
