#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is gator config file
# Do not change this file, use instance/gator.conf instead

HOST = "localhost"
PORT = 5000

BASE_URL = "http://localhost:5000"

DEBUG = True
TESTING = False

SECRET_KEY = "DuMmY sEcReT kEy"

CSRF_ENABLED = True
CSRF_SESSION_KEY = "_csrf_token"

MONGODB_SETTINGS = {
    "db": "gator",
    "host": "mongodb://localhost"
}

BABEL_DEFAULT_LOCALE = "en"

gator_NAME = "gator"
gator_PROVIDER = "gator"

LINKS_PER_PAGE = 50

# Google Analytics
GA_UA = "UA-XXXXXXXX-X"
