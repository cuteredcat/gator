#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from gator import db

class Media(db.Document):
    group = db.StringField(required=True)
    name = db.StringField(required=True)

    link = db.URLField(required=True, unique=True)
    tags = db.ListField(db.StringField(max_length=30))

    parser = db.StringField(required=True)
    last_update = db.DateTimeField()
    status = db.StringField()

    meta = {
        "indexes": ["group", "name", "tags"],
        "ordering": ["group", "name"]
    }

class Shares(db.EmbeddedDocument):
    social_network = db.StringField(required=True, unique=True)
    count = db.IntField(required=True)

    update = db.DateTimeField(default=datetime.now)
    change = db.IntField()

class News(db.Document):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    media = db.StringField(required=True)
    link = db.URLField(required=True, unique=True)
    text = db.StringField(required=True)
    tags = db.ListField(db.StringField(max_length=30))
    shares = db.ListField(db.EmbeddedDocumentField(Shares))

    meta = {
        "indexes": ["-created_at", "tags"],
        "ordering": ["-created_at"]
    }
