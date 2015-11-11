#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from gator import app, db
from gator.models import Media, News

import time

# create blueprint
core = Blueprint("core", __name__, template_folder="templates")

@core.route("/")
@core.route("/lastnews/")
@core.route("/lastnews/<string:delta>/")
def index(delta=None):
    return render_template("lastnews.html", delta=delta)

@core.route("/lastnews.json")
@core.route("/lastnews-<string:delta>.json")
def lastnews(delta=None):
    if delta == "today":
        end_time = datetime.now()
        start_time = end_time.replace(hour=0, minute=0, second=0, microsecond=0)
    elif delta == "yesterday":
        end_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_time = end_time - timedelta(days=1)
    elif delta == "week":
        end_time = datetime.now()
        start_time = end_time.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
    else:
        end_time = datetime.now()
        start_time = end_time - timedelta(days=1)

    return jsonify(news=News.objects(created_at__gt=start_time, created_at__lte=end_time).order_by("-shares__count")[:(app.config["LINKS_PER_PAGE"] * 4)])

@core.route("/timeline/", methods=['GET'])
@core.route("/timeline/page/<int:page>/", methods=['GET'])
@core.route("/timeline/<int:stamp>/", methods=['GET'])
@core.route("/timeline/<int:stamp>/page/<int:page>/", methods=['GET'])
def timeline(stamp=None, page=1):
    if not stamp:
        news = News.objects().paginate(page=page, per_page=app.config["LINKS_PER_PAGE"])
    else:
        if page > 1:
            news = News.objects(created_at__lte=datetime.utcfromtimestamp(stamp)).paginate(page=page, per_page=app.config["LINKS_PER_PAGE"])
        else:
            news = News.objects(created_at__gt=datetime.utcfromstimetamp(stamp)).paginate(page=page, per_page=app.config["LINKS_PER_PAGE"])

    stamp = time.time()

    if request.is_xhr:
        return jsonify(news=news.items, stamp=stamp)
    else:
        return render_template("timeline.html", news=news, stamp=stamp)

@core.route("/status/", methods=['GET'])
def status():
    medialist = Media.objects.all()
    return render_template("status.html", medialist=medialist)
