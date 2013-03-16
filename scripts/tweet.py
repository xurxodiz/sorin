#! /usr/bin/env python
# -*- coding: utf-8 -*-

import twitter
import sys

with open('scripts/SECRET', 'r') as f:
	[c_key, c_secret, a_key, a_secret] = f.readlines()

# careful! strip the endline!

api = twitter.Api(consumer_key=c_key.strip(),
                      consumer_secret=c_secret.strip(),
                      access_token_key=a_key.strip(),
                      access_token_secret=a_secret.strip())

if len(sys.argv) > 1:
	tweet = sys.argv[1]
else:
	tweet = sys.stdin.read().strip()

status = api.PostUpdate(tweet)

print tweet