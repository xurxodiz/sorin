#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
import json

with open("archive/"+sys.argv[1]+"/json", 'r') as f:
  chain = json.load(f)

curr = "\n"
numchars = -1 # offset the extra space counted in the first word
sentence = []
while (curr != False and numchars < 140):
  word = random.choice(chain[curr])
  if word: # only append if not false (i.e. not end of line)
    numchars += 1 + len(word)
    sentence.append(word)
  curr = word

# if we stopped because we exceeded size, we remove a word
if curr:
	sentence.pop()

sentence.reverse()
output = " ".join(sentence)

print(output.encode("utf-8"))