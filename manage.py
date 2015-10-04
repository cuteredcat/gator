#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager, Server, Shell

from gator import app
from parsers import Queue

manager = Manager(app)
queue = Queue()

manager.add_command("runserver", Server(host=app.config["HOST"], port=app.config["PORT"]))
manager.add_command("queue", queue.run())

manager.run()
