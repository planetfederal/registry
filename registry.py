import os
from django.conf import settings
from django.core import management
from django.conf.urls import url
from django.http import HttpResponse
from pycsw import server
from distutils.util import strtobool
from six import StringIO

__version__ = 0.1

DEBUG = strtobool(os.getenv('DEBUG', 'True'))
ROOT_URLCONF = 'registry'
DATABASES = {'default': {}}  # required regardless of actual usage
SECRET_KEY = os.getenv('SECRET_KEY', 'Please set a SECRET_KEY as an env var.')

if not settings.configured:
    settings.configure(**locals())


def csw_view(request, catalog=None):
    """CSW dispatch view.
       Wraps the WSGI call and allows us to tweak any django settings.
    """
    env = request.META.copy()
    env.update({'local.app_root': os.path.dirname(__file__),
                'REQUEST_URI': request.build_absolute_uri()})

    # Django hangs if we don't do wrap the body in StringIO
    if request.method == 'POST':
        env['wsgi.input'] = StringIO(request.body)

    csw = server.Csw(env)
    status, content = csw.dispatch_wsgi()
    response = HttpResponse(content,
                            content_type=csw.contenttype,
                            )

    return response


urlpatterns = [
    url(r'^$', csw_view),
    url(r'^(?P<catalog>\w+)?$', csw_view),
]


if __name__ == '__main__':  # pragma: no cover
    management.execute_from_command_line()
