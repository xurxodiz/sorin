#! /usr/bin/env python
# -*- coding: utf-8 -*-

import twitter
import sys

with open('scripts/SECRET', 'r') as f:
  [c_key, c_secret, a_key, a_secret] = f.readlines()

api = twitter.Api(consumer_key=c_key.strip(),
                      consumer_secret=c_secret.strip(),
                      access_token_key=a_key.strip(),
                      access_token_secret=a_secret.strip())

lines = []
subject = sys.argv[1]
maxid = None

for i in range(1,15):
	statuses = api.GetUserTimeline(user_id=subject, count=200, max_id=maxid)
	if statuses:
		for s in statuses:
			lines.append(s.text.encode("utf-8"))
		maxid = s.id-1

lines.reverse()
	
print maxid
print("\n".join(lines))