#! /usr/bin/env python
# -*- coding: utf-8 -*-

import twitter
import sys

api = twitter.Api()

lines = []
subject = sys.argv[1]
if sys.argv[2] == "back":
	sinceid, maxid = None, int(sys.argv[3])
else:
	maxid, sinceid = None, int(sys.argv[3])

for i in range(1,3):
	statuses = api.GetUserTimeline(id=subject, count=200, since_id=sinceid, max_id=maxid)
	if statuses:
		for s in statuses:
			lines.append(s.text.encode("utf-8"))
		if sys.argv[2] == "back":
			sinceid, maxid = None, s.id-1
		else:
			maxid, sinceid = None, s.id

if sys.argv[2] == "back":
	print(maxid)
else:
	print(sinceid)
	
print("\n".join(lines))