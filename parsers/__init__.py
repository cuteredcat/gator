#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from lxml.html import fromstring, make_links_absolute

from gator import db
from gator.models import Media, News

import cookielib, json, importlib, re, urllib, urllib2

RE_URL = re.compile(r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""")

class HTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        newreq = urllib2.HTTPRedirectHandler.redirect_request(self, req, fp, code, msg, headers, newurl)
        if newreq is not None: self.redirections.append(newreq.get_full_url())
        return newreq

class Batch():
    def __init__(self, parser=None):
        if parser:
            self.__run(parser)
        else:
            for media in Media.objects():
                self.__run(media.parser)

    def __run(self, name):
        parser = importlib.import_module("parsers.%s" % name)
        parser.grab(Parser)

class Parser():
    def __init__(self, charset='cp1251', *args, **kwargs):
        self.charset = charset
        self.cookie = cookielib.CookieJar()

        self.headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'),
                        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')]

        try:
            media = Media.objects.get(parser=kwargs.get("parser"))

            media.group = kwargs.get("group")
            media.name = kwargs.get("name")
            media.link = kwargs.get("link")
            media.tags = kwargs.get("tags", [])
            media.save()

        except db.DoesNotExist:
            media = Media(group=kwargs.get("group"),
                          name=kwargs.get("name"),
                          link=kwargs.get("link"),
                          tags=kwargs.get("tags", []),
                          parser=kwargs.get("parser"))
            media.save()

        self.media = media.parser
        self.id = media.id

    def grab(self, link, tree=True):
        try:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
            opener.addheaders = self.headers

            if isinstance(link, unicode):
                link = link.encode('utf-8')

            socket = opener.open(link)

            if self.charset is None:
                content = socket.read()
            else:
                content = unicode(socket.read(), self.charset)

            socket.close()

        except:
            content = None

        if content and tree:
            content = make_links_absolute(fromstring(content), link, resolve_base_href=True)

        return content

    def save(self, *args, **kwargs):
        # create record in News
        try:
            news = News(media=self.media,
                        link=kwargs.get("link"),
                        text=kwargs.get("text"),
                        tags=kwargs.get("tags", []))
            news.save()

        except db.NotUniqueError:
            pass

    def status(self, status):
        if self.id:
            media = Media.objects.get(id=self.id)

            media.last_update = datetime.now()
            media.status = status
            media.save()
