#!/usr/bin/env python
# -*- coding: utf-8 -*-

def grab(Parser):
    # init parser
    parser = Parser(group="Политика",
                    name="РИА Новости Украина",
                    link="http://rian.com.ua",
                    parser="rian_com_ua",
                    charset="utf-8")

    try:
        link = "http://rian.com.ua"
        page = parser.grab(link)
    except:
        parser.status("404")

    try:
        for el in reversed(page.cssselect(".main_news_list_items a")):
            href = el.get("href")
            text = u" ".join(el.xpath("./text()")).strip()

            if href and text:
                parser.save(link=href, text=text, tags=["fast"])

        parser.status("200")
    except:
        parser.status("500")
