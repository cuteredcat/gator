#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from gator import app, db
from gator.models import News

import time

# create blueprint
core = Blueprint("core", __name__, template_folder="templates")

@core.route("/", methods=['GET'])
@core.route("/<int:timestamp>/", methods=['GET'])
def index(timestamp=0):
    if timestamp:
        newslist = News.objects.filter(created_at__gt=datetime.utcfromtimestamp(timestamp))
    else:
        newslist = News.objects.all().paginate(page=1, per_page=app.config["LINKS_PER_PAGE"])

    timestamp = time.time()

    if request.is_xhr:
        return jsonify(newslist=newslist, timestamp=timestamp)
    else:
        return render_template("index.html", newslist=newslist, timestamp=timestamp)

@core.route("/<int:timestamp>/page/<int:page>/", methods=['GET'])
def more(timestamp, page):
    newslist = News.objects.filter(created_at__lte=datetime.utcfromtimestamp(timestamp)).paginate(page=page, per_page=app.config["LINKS_PER_PAGE"])
    timestamp = time.time()

    if request.is_xhr:
        return jsonify(newslist=newslist.items, timestamp=timestamp)
    else:
        return render_template("index.html", newslist=newslist, timestamp=timestamp)
