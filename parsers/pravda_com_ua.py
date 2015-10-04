#!/usr/bin/env python
# -*- coding: utf-8 -*-

def grab(Parser, db):
    # init parser
    parser = Parser()

    link = "http://www.pravda.com.ua"
    page = parser.grab(link)

    for el in page.cssselect("dl.mnews1 dd a"):
        href = el.get("href")
        text = el.text

        if href and text and not db.objects.filter(link=href):
            news = db(media="pravda_com_ua", link=href, text=text, tags=["fast"])
            news.save()
