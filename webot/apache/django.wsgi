
import os,sys

sys.path.append('/var/www/')
sys.path.append('/var/www/webot')
sys.path.append('/var/www/webot/webot')
os.environ['DJANGO_SETTINGS_MODULE'] = 'webot.settings'

import django.core.handlers.wsgi as django_wsgi
application = django_wsgi.WSGIHandler()

