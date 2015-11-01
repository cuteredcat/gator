#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gator import app

from shares import SocialNetwork

class Facebook(SocialNetwork):
    def get(self, link):
        separator = "?"
        if "?" in link:
            separator = "&"

        json = self.json("https://graph.facebook.com/v2.5/%s%sfields=share&access_token=%s" % (link, separator, app.config["FACEBOOK_ACCESS_TOKEN"]))

        if json:
            print json
