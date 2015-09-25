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
maxid = sys.maxsize # kinda hackish, i know

for i in range(1,15):
  statuses = t.statuses.user_timeline(screen_name=subject, count=200, max_id=maxid)
  if statuses:
    for s in statuses:
      lines.append(s['text'])
    maxid = s['id']-1

lines.reverse()

print(maxid)
print("\n".join(lines))
