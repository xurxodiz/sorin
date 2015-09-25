#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from twitter import *
import sys

with open('scripts/SECRET', 'r') as f:
  [c_key, c_secret, a_key, a_secret] = f.readlines()

t = Twitter(auth=OAuth(a_key.strip(),
                       a_secret.strip(),
                       c_key.strip(),
                       c_secret.strip()))

lines = []
subject = sys.argv[1]
sinceid = int(sys.argv[2])

for i in range(1,5):
	statuses = t.statuses.user_timeline(screen_name=subject, count=200, since_id=sinceid)
	if statuses:
		for s in statuses:
			lines.append(s['text'])
		sinceid = s['id']

lines.reverse()

print(sinceid)
print("\n".join(lines))
