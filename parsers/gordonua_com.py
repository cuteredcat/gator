#!/usr/bin/env python
# -*- coding: utf-8 -*-

def grab(Parser, db):
    # init parser
    parser = Parser(charset="utf-8")

    link = "http://gordonua.com"
    page = parser.grab(link)

    for el in reversed(page.cssselect("#rlab_0 li a")):
        href = el.get("href")
        text = u" ".join(el.xpath("./text()")).strip()

        if href and text and not db.objects.filter(link=href):
            news = db(media="gordonua_com", link=href, text=text, tags=["fast"])
            news.save()
