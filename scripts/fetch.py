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