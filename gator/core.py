#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from gator import app, db
from gator.models import Media, News

import time

# create blueprint
core = Blueprint("core", __name__, template_folder="templates")

@core.route("/", methods=['GET'])
@core.route("/<int:hours>-hours/", methods=['GET'])
@core.route("/<int:days>-days/", methods=['GET'])
def index(hours=None, days=None):
    return render_template("index.html", hours=hours, days=days)

@core.route("/page/<int:page>/", methods=['GET'])
@core.route("/<int:hours>-hours/page/<int:page>/", methods=['GET'])
@core.route("/<int:days>-days/page/<int:page>/", methods=['GET'])
def last(hours=None, days=None, page=1):
    if days:
        delta = timedelta(days=days)
    else:
        if not hours: hours = 6
        delta = timedelta(hours=hours)

    if request.is_xhr:
        news = News.objects(created_at__gt=(datetime.now() - delta)).order_by("-shares__count").paginate(page=page, per_page=app.config["LINKS_PER_PAGE"])
        return jsonify(news=news.items(), page=page)
    else:
        return redirect(url_for("core.index"))

@core.route("/timeline/", methods=['GET'])
@core.route("/timeline/page/<int:page>/", methods=['GET'])
@core.route("/timeline/<int:stamp>/", methods=['GET'])
@core.route("/timeline/<int:stamp>/page/<int:page>/", methods=['GET'])
def timeline(stamp=None, page=1):
    if not stamp:
        news = News.objects().paginate(page=page, per_page=app.config["LINKS_PER_PAGE"])
    else:
        if page > 1:
            news = News.objects(created_at__lte=datetime.utcfromstamp(stamp)).paginate(page=page, per_page=app.config["LINKS_PER_PAGE"])
        else:
            news = News.objects(created_at__gt=datetime.utcfromstamp(stamp)).paginate(page=page, per_page=app.config["LINKS_PER_PAGE"])

    stamp = time.time()

    if request.is_xhr:
        return jsonify(news=news.items, stamp=stamp)
    else:
        return render_template("index.html", news=news, stamp=stamp)

@core.route("/status/", methods=['GET'])
def status():
    medialist = Media.objects.all()
    return render_template("status.html", medialist=medialist)
