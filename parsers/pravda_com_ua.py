#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml.html import fromstring, make_links_absolute, tostring

from parsers import Parser

# init parser
parser = Parser()

def grab():
    link = 'http://www.pravda.com.ua'

    page = parser.grab(link)
    tree = make_links_absolute(fromstring(page), link, resolve_base_href=True)

    for element in tree.cssselect('dl.mnews1 dt, dl.mnews1 dd'):
        print element.text()
