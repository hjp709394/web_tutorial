import os
import sys

##Virtualenv Settings
activate_this = '/home/ubuntu/ve/py2/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

##Replace the standard out
sys.stdout = sys.stderr

##Add this file path to sys.path in order to import settings
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

##Add this file path to sys.path in order to import app
sys.path.append('/home/ubuntu/ws/web_tutorial/2.5._Paging')

##Create appilcation for our app
from demo import app as application
