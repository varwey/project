
import os,sys

sys.path.append('/var/www')
sys.path.append('/var/www/yqzbw')
sys.path.append('/var/www/yqzbw/yqzbw')

os.environ['DJANGO_SETTINGS_MODULE'] = 'yqzbw.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
