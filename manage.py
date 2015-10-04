#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Command, Manager, Server, Shell

from gator import app

class Tasks(Command):
    option_list = (
        Option('--module', '-m', dest='module'),
    )

    def run(self, module):
        from gator.models import News
        from parsers import Parser

        grab = importlib.import_module('parsers.%s.grab' % module)
        grab(Parser(), News)

manager = Manager(app)
manager.add_command("runserver", Server(host=app.config["HOST"], port=app.config["PORT"]))
manager.add_command("tasks", Tasks())

manager.run()
