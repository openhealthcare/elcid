"""
WSGI config for elcid project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "elcid.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elcid.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)


import static

from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.contrib.staticfiles.handlers import StaticFilesHandler as DebugHandler

try:
    from urllib.parse import urlparse
except ImportError:     # Python 2
    from urlparse import urlparse
from django.contrib.staticfiles import utils

try:
    from django.core.handlers.wsgi import get_path_info
except ImportError:  # django < 1.7
    try:
        from django.core.handlers.base import get_path_info
    except ImportError:     # django < 1.5
        import sys
        py3 = sys.version_info[0] == 3

        def get_path_info(environ):
            """
            Returns the HTTP request's PATH_INFO as a unicode string.
            """
            path_info = environ.get('PATH_INFO', str('/'))
            # Under Python 3, strings in environ are decoded with ISO-8859-1;
            # re-encode to recover the original bytestring provided by the web server.
            if py3:
                path_info = path_info.encode('iso-8859-1')
            # It'd be better to implement URI-to-IRI decoding, see #19508.
            return path_info.decode('utf-8')


try:
    # Serve static files on Heroku
    from dj_static import Cling
    from static import Cling as StaticCling

    class DebugDJStatic(Cling):
        def __call__(self, environ, start_response):
            # Hand non-static requests to Django
            print "starting debug dj static %s %s" % (environ, start_response)

            if not self._should_handle(get_path_info(environ)):
                print "should not handle"
                return self.application(environ, start_response)

            # Serve static requests from static.Cling
            if not self.debug or self.ignore_debug:
                print "not on debug"
                path_info = environ.get('PATH_INFO', '')
                full_path = self.cling._full_path(path_info)
                print "full path %s" % full_path
                print "under full root %s" % self.cling._is_under_root(full_path)
                environ = self._transpose_environ(environ)
                return self.cling(environ, start_response)
            # Serve static requests in debug mode from StaticFilesHandler
            else:
                print "on debug"
                return self.debug_cling(environ, start_response)



    application = DebugDJStatic(get_wsgi_application())
except ImportError:
    application = get_wsgi_application()
