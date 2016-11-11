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
def is_subtweet(haystack, needle):
    """
    Source: http://codereview.stackexchange.com/questions/19627/finding-sub-list
    Return the index at which the sequence needle appears in the
    sequence haystack, or -1 if it is not found, using the Boyer-
    Moore-Horspool algorithm. The elements of needle and haystack must
    be hashable.

    >>> find([1, 1, 2], [1, 2])
    1

    """
    for hay in haystack:
      h = len(hay)
      n = len(needle)
      skip = {needle[i]: n - i - 1 for i in range(n - 1)}
      i = n - 1
      while i < h:
          for j in range(n):
              if hay[i - j] != needle[-j - 1]:
                  i += skip.get(hay[i], n)
                  break
          else:
              #return i - n + 1
              return True
      #return -1
    return False
###


###
# generate a tweet based on the 1-gram and 2-gram chains
# and check against existing and past generated tweets
def generate(maxlen, chains, odds=None):
  numchars = -1 # offset the extra space counted in the first word
  sentence = []
  while True:
    try:
      if odds:
        ngram = random.choice(odds)
      else:
        ngram = random.choice(list(chains.keys()))
      choices = chains[ngram]
      while ngram:
        w = sentence[-ngram] if len(sentence) > (ngram-1) else ""
        choices = choices[w]
        ngram -= 1
    except KeyError:
      choices = []
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
  return sentence


def generate_with_checks(maxlen, chains, backlog, odds=None):
  while True:
    output = generate(maxlen, chains, odds)
    if not is_subtweet(backlog, output):
      break
  return output


if __name__ == "__main__":

  chains = {}

  with open("archive/"+sys.argv[1]+"/json", 'r') as f:
    chains[1] = json.load(f)

  with open("archive/"+sys.argv[1]+"/json2", 'r') as f:
    chains[2] = json.load(f)

  with open("archive/"+sys.argv[1]+"/log", 'r') as f:
    tweets = [l.strip() for l in f.readlines()]

  try:
    with open("archive/"+sys.argv[1]+"/past", 'r+') as f:
      past = [l.strip() for l in f.readlines()]
  except IOError:
      past = []

  backlog = [s.split(" ") for s in tweets+past]
  output = generate_with_checks(140, chains, backlog, [1, 2, 2])
  # we leave ! and ? since they make sense isolated
  output = [w.translate(str.maketrans('', '', '"()[]{}«»¡¿')) for w in output]
  output = " ".join(output)
  output = xml.sax.saxutils.unescape(output)

  print(output)

  with open("archive/"+sys.argv[1]+"/past", 'a+') as f:
    f.write(output+"\n")
