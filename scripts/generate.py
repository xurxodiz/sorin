#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
import json

with open("archive/"+sys.argv[1]+"/json", 'r') as f:
  chain = json.load(f)

with open("archive/"+sys.argv[1]+"/log", 'r') as f:
  tweets = [l.split() for l in f.readlines()]

output = tweets[0] # hack to guarantee a first iteration
while output in tweets:

  curr = "\n"
  numchars = -1 # offset the extra space counted in the first word
  sentence = []
  banned = [[]]
  while True:
    choices = [x for x in chain[curr] if x not in banned[-1]]
    if [] == choices:
      #if len(banned) > 1:
      banned.pop() 
      #if len(sentence) > 0:
      previous = sentence.pop()
      banned[-1].append(curr)
      numchars = numchars - 1 - len(curr)
      curr = previous
      continue
    word = random.choice(choices)
    if not word:
      break # end of sentence
    else:
      if (numchars + 1 + len(word)) >= 140:
        banned[-1].append(word)
        continue
      else:
        numchars += 1 + len(word)
        sentence.append(word)
        banned.append([])
        curr = word
  output = " ".join(sentence)

print(output.encode("utf-8"))