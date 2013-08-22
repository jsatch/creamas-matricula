import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'Creamas.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

path = '/home/devos/Aplicaciones/Creamas/'
if path not in sys.path:
    sys.path.append(path)
