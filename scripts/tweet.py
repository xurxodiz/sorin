#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from twitter import *
import sys

with open('scripts/SECRET', 'r') as f:
	[c_key, c_secret, a_key, a_secret] = f.readlines()

# careful! strip the endline!

t = Twitter(auth=OAuth(a_key.strip(),
                       a_secret.strip(),
                       c_key.strip(),
                       c_secret.strip()))

if len(sys.argv) > 1:
	tweet = sys.argv[1]
else:
	tweet = sys.stdin.read().strip()

t.statuses.update(status=tweet)

print(tweet)
