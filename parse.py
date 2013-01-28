#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys

with open("archive/"+sys.argv[1]+"/log") as f:
  chain = {}

  for tweet in f:
    words = tweet.split()
    curr = "\n"
    for word in words:
      chain.setdefault(curr,[]).append(word)
      curr = word
    chain.setdefault(curr,[]).append(False)

with open("archive/"+sys.argv[1]+"/json", 'w') as f:
  json.dump(chain, f, indent=2, separators=(',', ': '), sort_keys=True)