#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Command, Manager, Option, Server, Shell

from gator import app

class Parse(Command):
    option_list = (Option('--parser', '-p', dest='parser'))

    def run(self, parser):
        from parsers import Batch
        batch = Batch(parser)

manager = Manager(app)
manager.add_command("runserver", Server(host=app.config["HOST"], port=app.config["PORT"]))
manager.add_command("parse", Parse())

manager.run()
