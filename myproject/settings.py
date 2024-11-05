import os
import sys

# Añadir la ruta de tu proyecto al path
path = '/home/jfplata/mysiteTest'
if path not in sys.path:
    sys.path.append(path)

# Configurar las variables de entorno
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
