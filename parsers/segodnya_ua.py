#!/usr/bin/env python
# -*- coding: utf-8 -*-

def grab(Parser, db):
    # init parser
    parser = Parser(charset="utf-8")

    link = "http://segodnya.ua"
    page = parser.grab(link)

    for el in reversed(page.cssselect(".content .main_side .items a.news_text")):
        href = el.get("href")
        text = u" ".join(el.xpath("./text()")).strip()

        if href and text and not db.objects.filter(link=href):
            news = db(media="segodnya_ua", link=href, text=text, tags=["fast"])
            news.save()
