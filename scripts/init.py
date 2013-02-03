#! /usr/bin/env python
# -*- coding: utf-8 -*-

import twitter
import sys

api = twitter.Api()

lines = []
subject = sys.argv[1]
maxid = None

for i in range(1,15):
	statuses = api.GetUserTimeline(id=subject, count=200, max_id=maxid)
	if statuses:
		for s in statuses:
			lines.append(s.text.encode("utf-8"))
		maxid = s.id-1

lines.reverse()
	
print maxid
print("\n".join(lines))