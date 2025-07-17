import sys, os

# Define o diretório raiz do projeto
sys.path.insert(0, os.path.dirname(__file__))

# Nome do seu módulo de configurações (verifique se é exatamente isso)
os.environ['DJANGO_SETTINGS_MODULE'] = 'prospapp.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()