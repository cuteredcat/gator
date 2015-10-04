#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Command, Manager, Option, Server, Shell

import importlib

from gator import app

class Tasks(Command):
    option_list = (
        Option('--parser', '-p', dest='parser'),
    )

    def run(self, parser):
        if parser:
            self.parser(parser)

    def parser(self, name):
        from gator.models import News
        from parsers import Parser

        parser = importlib.import_module('parsers.%s' % name)
        parser.grab(Parser, News)

manager = Manager(app)
manager.add_command("runserver", Server(host=app.config["HOST"], port=app.config["PORT"]))
manager.add_command("tasks", Tasks())

manager.run()
