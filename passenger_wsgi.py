import sys, os
sys.path.insert(0, os.path.dirname(__file__))

os.environ['DJANGO_SETTINGS_MODULE'] = 'prospapp.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()