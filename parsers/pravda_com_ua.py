#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml.html import fromstring, make_links_absolute, tostring

from gator.models import News
from parsers import Parser

# init parser
parser = Parser()
queue = Queue()

def grab():
    link = "http://www.pravda.com.ua"

    page = parser.grab(link)
    tree = make_links_absolute(fromstring(page), link, resolve_base_href=True)

    for el in tree.cssselect("dl.mnews1 dd a"):
        href = el.get("href")
        text = el.text

        if href and text and not News.objects.filter(link=href):
            news = News(media="pravda_com_ua", link=href, text=text, tags=["fast"])
            news.save()

queue.register("pravda_com_ua", grab)
