import sys, os

# Caminho da raiz do projeto Django
sys.path.insert(0, "/home/prospere/prospapp")

# Nome do módulo de configurações do Django
os.environ["DJANGO_SETTINGS_MODULE"] = "prospapp.settings"

# Importa a aplicação WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()