import os
import sys
import site
from django.core.wsgi import get_wsgi_application

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/var/www/okota.co.za/env/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/var/www/okota.co.za/okota')
sys.path.append('/var/www/okota.co.za/okota/okota_website')

os.environ['DJANGO_SETTINGS_MODULE'] = 'okota_website.settings'

# Activate your virtual env
activate_env=os.path.expanduser("/var/www/okota.co.za/env/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))


application = get_wsgi_application()

