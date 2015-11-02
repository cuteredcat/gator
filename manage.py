#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Command, Manager, Option, Server, Shell

from gator import app

class Parse(Command):
    option_list = (Option('--parser', '-p', dest='parser'),)

    def run(self, parser):
        from parsers import Batch
        batch = Batch(parser)

class Share(Command):
    option_list = (Option('--share', '-s', dest='share'),)

    def run(self, share):
        if share == "facebook":
            from shares.facebook import Facebook
            fb = Facebook()
            fb.run()

manager = Manager(app)
manager.add_command("runserver", Server(host=app.config["HOST"], port=app.config["PORT"]))
manager.add_command("parse", Parse())
manager.add_command("share", Share())

manager.run()
