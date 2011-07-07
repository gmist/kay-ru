# -*- coding: utf-8 -*-

"""
Kay test settings.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

DEBUG = False
ROOT_URL_MODULE = 'kay.tests.globalurls'

MIDDLEWARE_CLASSES = (
  'kay.sessions.middleware.SessionMiddleware',
  'kay.auth.middleware.AuthenticationMiddleware',
)

INSTALLED_APPS = (
  'kay.tests',
)

APP_MOUNT_POINTS = {
  'kay.tests': '/',
}

AUTH_USER_BACKEND = "kay.auth.backends.datastore.DatastoreBackend"
AUTH_USER_MODEL = "kay.auth.models.DatastoreUser"
