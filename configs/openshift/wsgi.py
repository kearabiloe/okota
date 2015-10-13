#!/usr/bin/python
import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'okota_website.settings'
sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi',
    'okota_website'))

virtenv = os.environ['OPENSHIFT_HOMEDIR'] + '/virtenv/'
os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib/python2.6/site-packages')
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')

try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass

#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()