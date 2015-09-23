#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager, Server, Shell
from gator import app

manager = Manager(app)

manager.add_command("runserver", Server(host=app.config["HOST"], port=app.config["PORT"]))
manager.run()
