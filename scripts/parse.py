#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

with open("archive/"+sys.argv[1]+"/log") as f:
  chain = {}

  for tweet in f:
    words = tweet.strip().split()
    curr = u"\n"
    for word in words:
      chain.setdefault(curr,[]).append(word)
      curr = word
    chain.setdefault(curr,[]).append(False)

with open("archive/"+sys.argv[1]+"/json", 'w') as f:
  json.dump(chain, f, indent=2, sort_keys=True, ensure_ascii=False)