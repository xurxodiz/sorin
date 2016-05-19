#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
import json
import xml.sax.saxutils
import random


####
# jump back a random distance
def backjump(sentence, numchars):
  cutpoint = random.randint(0, len(sentence))
  for i in range(0, cutpoint):
    popped = sentence.pop()
    numchars = numchars - 1 - len(popped)
  return sentence, numchars
####


###
# check if a string is a verbatim part of an exiting tweet
def is_subtweet(tweets, s):
  return any([tt.find(s) != -1 for tt in tweets])
###


###
# generate a tweet based on the 1-gram and 2-gram chains
# and check against existing and past generated tweets
def generate(maxlen, chain, chain2):
  numchars = -1 # offset the extra space counted in the first word
  sentence = []
  while True:
    prev = sentence[-2] if len(sentence) > 1 else "\n"
    curr = sentence[-1] if len(sentence) > 0 else "\n"
    if random.choice([True, False, False]):
      choices = [x for x in chain[curr]]
    else:
      choices = [x for x in chain2[prev+" "+curr]]
    if [] == choices:
      sentence, numchars = backjump(sentence, numchars)
      continue
    word = random.choice(choices)
    if not word:
      break # end of sentence
    else:
      if (numchars + 1 + len(word)) >= maxlen:
        sentence, numchars = backjump(sentence, numchars)
        continue
      else:
        numchars += 1 + len(word)
        sentence.append(word)
  return " ".join(sentence)


def generate_with_checks(maxlen, chain, chain2, tweets, past):
  output = tweets[0] # hack to guarantee a first iteration
  while is_subtweet(tweets, output) or output in past:
    output = generate(maxlen, chain, chain2)

  # we leave ! and ? since they make sense isolated
  output = [w.translate(str.maketrans('', '', '"()[]{}«»¡¿')) for w in output.split()]
  output = " ".join(output)
  output = xml.sax.saxutils.unescape(output)

  return output


if __name__ == "__main__":

  with open("archive/"+sys.argv[1]+"/json", 'r') as f:
    chain = json.load(f)

  with open("archive/"+sys.argv[1]+"/json2", 'r') as f:
    chain2 = json.load(f)

  with open("archive/"+sys.argv[1]+"/log", 'r') as f:
    tweets = [l.strip() for l in f.readlines()]

  try:
    with open("archive/"+sys.argv[1]+"/past", 'r+') as f:
      past = [l.strip() for l in f.readlines()]
  except IOError:
      past = []

  output = generate_with_checks(140, chain, chain2, tweets, past)

  print(output)

  with open("archive/"+sys.argv[1]+"/past", 'a+') as f:
    f.write(output+"\n")
