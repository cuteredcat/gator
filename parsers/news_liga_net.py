#!/usr/bin/env python
# -*- coding: utf-8 -*-

def grab(Parser):
    # init parser
    parser = Parser(group=u"Политика",
                    name=u"ЛІГА.Новости",
                    link=u"http://news.liga.net",
                    parser=u"news_liga_net",
                    charset="utf-8")

    try:
        link = "http://news.liga.net"
        page = parser.grab(link)
    except:
        parser.status("404")

    try:
        for el in reversed(page.cssselect(".last_news_list ul li a:first-child")):
            href = el.get("href")
            text = u" ".join(el.xpath("./text()")).strip()

            if href and text:
                parser.save(link=href, text=text, tags=["fast"])

        parser.status("200")
    except:
        parser.status("500")
