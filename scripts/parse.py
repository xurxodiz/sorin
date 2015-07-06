#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

with open("archive/"+sys.argv[1]+"/log") as f:
  chain = {}
  chain2 = {}

  for tweet in f:
    words = tweet.strip().split()
    prev = u"\n"
    curr = u"\n"
    for word in words:
      chain.setdefault(curr,[]).append(word)
      chain2.setdefault(prev+" "+curr,[]).append(word)
      prev = curr
      curr = word
    chain.setdefault(curr,[]).append(False)
    chain2.setdefault(prev+" "+curr,[]).append(False)

with open("archive/"+sys.argv[1]+"/json", 'w') as f:
  json.dump(chain, f, indent=2, sort_keys=True, ensure_ascii=False)

with open("archive/"+sys.argv[1]+"/json2", 'w') as f:
  json.dump(chain2, f, indent=2, sort_keys=True, ensure_ascii=False)
