#from __future__ import absolute_import # optional, but I like it
from .common import *

# Development overrides
DEBUG = False
ENVIRONMENT = "PROD"

# make all loggers use the file & make sure debugging is turned to warning.
for logger in LOGGING['loggers']:
    # LOGGING['loggers'][logger]['handlers'] = ['file']
    if LOGGING['loggers'][logger]['level'] == 'DEBUG':
        LOGGING['loggers'][logger]['level'] = 'ERROR'

