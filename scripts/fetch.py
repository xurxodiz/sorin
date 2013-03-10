#! /usr/bin/env python
# -*- coding: utf-8 -*-

import twitter
import sys

api = twitter.Api()

lines = []
subject = sys.argv[1]
sinceid = int(sys.argv[2])

for i in range(1,5):
	statuses = api.GetUserTimeline(id=subject, count=200, since_id=sinceid)
	if statuses:
		for s in statuses:
			lines.append(s.text.encode("utf-8"))
		sinceid = s.id

print(sinceid)
lines.reverse()
print("\n".join(lines))