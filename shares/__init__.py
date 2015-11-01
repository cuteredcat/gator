#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from time import sleep

from gator import db
from gator.models import News, Shares

import cookielib, json, urllib2

class SocialNetwork():
    def __init__(self):
        self.cookie = cookielib.CookieJar()
        self.headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'),
                        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')]

    def json(self, link):
        try:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
            opener.addheaders = self.headers

            if isinstance(link, unicode):
                link = link.encode('utf-8')

            socket = opener.open(link)
            content = socket.read()
            socket.close()

            return json.loads(content)

        except:
            return None

    def run(self):
        i = 1
        while i:
            if i % 256 == 0: self.__update(9)
            elif i % 128 == 0: self.__update(8)
            elif i % 64 == 0: self.__update(7)
            elif i % 32 == 0: self.__update(6)
            elif i % 16 == 0: self.__update(5)
            elif i % 8 == 0: self.__update(4)
            elif i % 4 == 0: self.__update(3)
            elif i % 2 == 0: self.__update(2)
            else: self.__update(1)

            i += 1
            sleep(self.check_interval)

    def update(self, start, end):
        news = News.objects(created_at__gt=end,
                            created_at__lte=start,
                            shares__social_network__ne=self.name).first()

        if news:
            count = self.get(news.link)

            news.shares.create(social_network=self.name,
                               count = count,
                               update = datetime.now(),
                               change = count)

            news.save()

        else:
            news = News.objects(created_at__gt=end,
                                created_at__lte=start).order_by('shares__update').first()

            if news:
                count = self.get(news.link)

                try:
                    social_network = news.shares.get(social_network=self.name)

                    social_network.count += count
                    social_network.update = datetime.now()
                    social_network.change = count
                    social_network.save()

                except db.DoesNotExist:
                    pass

    def __update(self, lvl):
        if lvl == 1: start = datetime.now()
        else: start = datetime.now() - timedelta(hours=2**(lvl-1))

        end = datetime.now() - timedelta(hours=2**lvl)
        self.update(start, end)
