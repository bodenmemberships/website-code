import os

gettext = lambda s: s
"""
Django settings for mainsite project.

Generated by 'django-admin startproject' using Django 1.8.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/

See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

"""
# APP_DIR is the main application directory (mainsite for us)
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# PROJECT_DIR is the directory that is the django project (website for us)
PROJECT_DIR = os.path.dirname(APP_DIR)
# BASE_DIR: is whatever directory contains your environment and project directory (djangocms for me)
BASE_DIR = os.path.dirname(PROJECT_DIR)
# DATA_DIR: is the directory containing our data (database? staticfiles? media?)
DATA_DIR = os.path.join(BASE_DIR, 'website_content')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@$%x*kpb@)n3tmc$7k^lb18aovbmp&g+ai7@py0rd*)4g(a(_7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
ROOT_URLCONF = 'mainsite.urls'
WSGI_APPLICATION = 'mainsite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media/')
STATIC_ROOT = os.path.join(BASE_DIR, 'website_static')

STATICFILES_DIRS = (
)
SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(APP_DIR, 'templates'), ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.i18n',
                'django.core.context_processors.debug',
                'django.core.context_processors.request',
                'django.core.context_processors.media',
                'django.core.context_processors.csrf',
                'django.core.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.core.context_processors.static',
                'cms.context_processors.cms_settings',
                'mainsite.context_processors.spe_context.set_default_values',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader'
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'mainsite.middleware.visitor.VisitorMiddleware',
    'request.middleware.RequestMiddleware',
)

INSTALLED_APPS = (
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'ckeditor',
    'ckeditor_uploader',
    'djangocms_style',
    'djangocms_column',
    'djangocms_file',
    'djangocms_googlemap',
    'djangocms_inherit',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_teaser',
    'djangocms_video',
    'easy_select2',
    'reversion',
    'mainsite',
    'segmentation',
    'smartsnippets',
    'taggit',
    'spe_links',
    'spe_blog',
    'google_tag_manager',
    'spe_contact',
    'spe_polls',
    'spe_styledlink',
    'request',
)

LANGUAGES = (
    # Customize this
    ('en', gettext('en')),
    ('es', gettext('es')),
    ('ru', gettext('ru')),
)

CMS_LANGUAGES = {
    # Customize this
    'default': {
        'public': True,
        'hide_untranslated': False,
        'redirect_on_fallback': True,
    },
    1: [
        {
            'public': True,
            'code': 'en',
            'hide_untranslated': False,
            'name': gettext('en'),
            'redirect_on_fallback': True,
        },
        {
            'public': True,
            'code': 'es',
            'hide_untranslated': False,
            'name': gettext('es'),
            'redirect_on_fallback': True,
        },
        {
            'public': True,
            'code': 'ru',
            'hide_untranslated': False,
            'name': gettext('ru'),
            'redirect_on_fallback': True,
        },
    ],
}

CMS_TEMPLATES = (
    # Customize this
    ('www_3col.html', 'WWW 3 Column page. Homepage'),
    ('ogf_home.html', 'OGF Homepage'),
    ('ogf_subpage.html', 'OGF SubPage'),
    # ('spe_3col.html', 'SPE 3 Column page. Homepage'),
    # ('page.html', '1 Column Page'),
    # ('feature.html', '1 Column Page with Feature'),
    # ('2column.html', '2 Column Page'),
    # ('3column.html', '3 Column Page'),
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

MIGRATION_MODULES = {

}

TAGGIT_CASE_INSENSITIVE = True
CKEDITOR_UPLOAD_PATH = os.path.join(DATA_DIR, 'ck_media')
GEOIP_PATH = os.path.join(PROJECT_DIR, 'data', 'GeoIP')
# LOGFILE_NAME = os.path.join(BASE_DIR, 'output.log')

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': LOGFILE_NAME,
        #     'formatter': 'verbose'
        #     },
    },
    'loggers': {
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'website': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

EMAIL_HOST = "relaydev.spe.org"
EMAIL_DEFAULT_FROM = "support@spe.org"
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
MANAGERS = (('IT', 'webmaster@spe.org'), )

CKEDITOR_CONFIGS = {
    "default": {
        'removePlugins': 'stylesheetparser',
        'allowedContent': True,
    }
}
# CKEDITOR_SETTINGS = {
#         "allowedContent": True
# }

SPE_STYLEDLINK_MODELS = [
    {
        'type': 'CMS Pages',
        'class_path': 'cms.models.Page',
        'manager_method': 'public',
        'filter': { 'publisher_is_draft': False },
    }
]

#REQUEST_TRAFFIC_MODULES = (
#    'request.traffic.UniqueVisitor',
#    'request.traffic.UniqueVisit',
#    'request.traffic.Hit',
#    'request.traffic.Ajax',
#    'request.traffic.NotAjax',
#    'request.traffic.Error',
#    'request.traffic.Error404',
#    'request.traffic.Search',
#    'request.traffic.Secure',
#    'request.traffic.Unsecure',
#    'request.traffic.User',
#    'request.traffic.UniqueUser',
#)

REQUEST_PLUGINS = (
    'request.plugins.TrafficInformation',
    'request.plugins.LatestRequests',

    'request.plugins.TopPaths',
    'request.plugins.TopErrorPaths',
    'request.plugins.TopReferrers',
    'request.plugins.TopSearchPhrases',
    'request.plugins.TopBrowsers',
    'request.plugins.ActiveUsers',
)
