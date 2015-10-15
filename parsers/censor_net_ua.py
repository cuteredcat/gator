#!/usr/bin/env python
# -*- coding: utf-8 -*-

def grab(Parser):
    # init parser
    parser = Parser(group=u"Политика",
                    name=u"Цензор.НЕТ",
                    link=u"http://censor.net.ua",
                    parser=u"censor_net_ua",
                    charset="utf-8")

    try:
        link = "http://censor.net.ua"
        page = parser.grab(link)
    except:
        parser.status("404")

    try:
        for el in reversed(page.cssselect("#w10 .curpane article header a")):
            href = el.get("href")
            text = u" ".join(el.xpath("./text()")).strip()

            if href and text:
                parser.save(link=href, text=text, tags=["fast"])

        parser.status("200")
    except:
        parser.status("500")
