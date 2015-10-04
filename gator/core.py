#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, redirect, render_template, request, url_for

from gator import db
from gator.models import News

# create blueprint
core = Blueprint("core", __name__, template_folder="templates")

@core.route("/", methods=['GET'])
@core.route("/page/<int:page>/", methods=['GET'])
def index(page=1):
    newslist = News.objects.filter(created_at__gte = date).paginate(page=1, per_page=app.config["LINKS_PER_PAGE"])
    return render_template("index.html", newslist=newslist)
