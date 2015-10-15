#!/usr/bin/env python
# -*- coding: utf-8 -*-

def grab(Parser):
    # init parser
    parser = Parser(group=u"Политика",
                    name=u"УНИАН",
                    link=u"http://www.unian.net",
                    parser=u"unian_net",
                    charset="utf-8")

    try:
        link = "http://www.unian.net"
        page = parser.grab(link)
    except:
        parser.status("404")

    try:
        for el in reversed(page.cssselect(".main_all_news li a")):
            href = el.get("href")
            text = u" ".join(el.xpath("./text()")).strip()

            if href and text:
                parser.save(link=href, text=text, tags=["fast"])

        parser.status("200")
    except:
        parser.status("500")
