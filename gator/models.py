#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from gator import db

class News(db.Document):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    media = db.StringField(required=True)
    link = db.URLField(required=True, unique=True)
    text = db.StringField(required=True)
    tags = db.ListField(db.StringField(max_length=30))

    meta = {
        "indexes": ["-created_at", "tags"],
        "ordering": ["-created_at"]
    }
