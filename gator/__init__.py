#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.babel import Babel, format_timedelta

from gator import settings

# init application
app = Flask("gator", instance_relative_config=True)
app.config.from_object(settings)
app.config.from_pyfile("gator.conf", silent=True)

# init db
db = MongoEngine(app)

# init localization
babel = Babel(app)

# before import blueprints we need to init db
from gator.core import core
#from gator.admin import admin

# register blueprints
app.register_blueprint(core)
#app.register_blueprint(admin)

@app.template_filter("timedelta")
def timedelta_filter(value):
    return format_timedelta(value)

if __name__ == "__main__":
    app.run()
