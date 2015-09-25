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
maxid = None

for i in range(1,15):
  if maxid:
    statuses = t.statuses.user_timeline(screen_name=subject, count=200,
      include_rts=False, exclude_replies=True, trim_user=True, max_id=maxid)
  else:
    statuses = t.statuses.user_timeline(screen_name=subject, count=200,
      include_rts=False, exclude_replies=True, trim_user=True)
  if statuses:
    for s in statuses:
      lines.append(s['text'])
    maxid = s['id']-1

lines.reverse()

print(maxid)
print("\n".join(lines))
