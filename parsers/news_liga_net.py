#!/usr/bin/env python
# -*- coding: utf-8 -*-

def grab(Parser, db):
    # init parser
    parser = Parser(charset="utf-8")

    link = "http://news.liga.net"
    page = parser.grab(link)

    for el in reversed(page.cssselect(".last_news_list ul li a:first-child")):
        href = el.get("href")
        text = u" ".join(el.xpath("./text()")).strip()

        if href and text and not db.objects.filter(link=href):
            news = db(media="news_liga_net", link=href, text=text, tags=["fast"])
            news.save()