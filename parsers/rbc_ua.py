#!/usr/bin/env python
# -*- coding: utf-8 -*-

def grab(Parser, db):
    # init parser
    parser = Parser(charset="utf-8")

    link = "http://www.rbc.ua"
    page = parser.grab(link)

    for el in page.cssselect("#pane ul a"):
        href = el.get("href")
        text = u" ".join(el.xpath("./text()")).strip()

        if href and text and not db.objects.filter(link=href):
            print text
            #news = db(media="rbc_ua", link=href, text=text, tags=["fast"])
            #news.save()
