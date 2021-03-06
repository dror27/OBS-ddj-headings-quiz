#!/usr/bin/env python

from pymongo import MongoClient
import pymongo
import feedparser
from pprint import pprint
import datetime

import core.db

# open database connection
db = core.db.get_db()

# loop on sources
for source in db.sources.find():

    if "userAgent" in source:
        feed = feedparser.parse(source["rss"], agent=source["userAgent"])
    else:
        feed = feedparser.parse(source["rss"])
    print(feed.href, len(feed.entries))
    
    for entry in feed.entries:
        entry["_source"] = source
        entry["_fetched"] = datetime.datetime.utcnow()
        entry["_timestamp"] = datetime.datetime(*entry["published_parsed"][0:6]) if "published_parsed" in entry else entry["_fetched"]
        
        key = {"id": entry.id}
        db.headings.replace_one(key, entry, True)
