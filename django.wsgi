import os, sys
path = '/var/www/checkreg'

if path not in sys.path:
	sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'checkreg.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

