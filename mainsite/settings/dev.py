#from __future__ import absolute_import # optional, but I like it
from .common import *

# Development overrides

DEBUG = True
ENVIRONMENT = "DEV"

# Overriding the templates in development to include a test page
CMS_TEMPLATES += (
    ('test.html', 'Test Page'),
)

# make all loggers use the console.
for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['handlers'] = ['console']

