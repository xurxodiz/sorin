#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import sys

class Markov:

  def __init__(self, corpusFile=None, corpusStdin=False, corpus=[], chainsFile=None, chains={}, delimiter=" ", sentenceDelimiter="\n", odds=[], backlogFile=None, backlog=[]):

    self.__delimiter = delimiter
    self.__sentence_delimiter = sentenceDelimiter
    self.__odds = odds

    if backlogFile:
      self.load_backlog(backlogFile)
    else:
      self.__backlog = backlog

    if corpusStdin:
      self.load_corpus("") # will read from stdin
    elif corpusFile:
      self.load_corpus(corpusFile)
    else:
      self.__corpus = corpus

    if chainsFile:
      self.load_chains(chainsFile)
    else:
      self.__chains = chains

    # only useful odds are those in chain keys
    if self.__odds and self.__chains.keys():
      self.__odds = [o for o in self.__odds if o in list(self.__chains.keys())]

    # if that resulted in no odds, we take the chain keys directly
    if not self.__odds and self.__chains.keys():
      self.__odds = list(self.__chains.keys())

    # if both are absent, default
    if not self.__odds:
      self.__odds = [1]

    if not self.__chains:
      if self.__corpus:
        self.make_chains(list(set(self.__odds)))
      else:
        raise ArgumentError("Either corpus or chains need to be provided")


  def load_corpus(self, filepath):
    self.__corpus = self.__load_file(filepath)
    return None


  def load_backlog(self, filepath):
    self.__backlog = self.__load_file(filepath)
    return None


  def __load_file(self, filepath):
    with open(filepath, 'r', encoding='utf-8') if filepath else sys.stdin as f:
      txt = f.read().split(self.__sentence_delimiter)
      if not self.__delimiter:
        return [list(l) for l in txt] # split every character
      else:
        return [l.split(self.__delimiter) for l in txt]


  def load_chains(self, filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
      self.__chains = json.load(f)

    # top-level ngram dict-keys changed to int because it's more intuitive
    # json only allows strings, so we convert it here
    self.__chains = {int(k): v for k,v in self.__chains.items()}
    return None


  def save_chains(self, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
      return json.dump(self.__chains, f, indent=2, sort_keys=True, ensure_ascii=False)


  def __ix(self, array, pos):
    # don't wrap around: empty strings before string
    if pos < 0:
      return ""
    try:
      return array[pos]
    except IndexError:
      return ""


  def make_chains(self, ngrams):

    for sentence in self.__corpus:
      # add False at end as EOF
      for i, word in enumerate(sentence + [False]):
        # for each n-gram level
        for n in ngrams:
          # key has to be str because json
          ch = self.__chains.setdefault(n, {})
          c = n
          # traverse the tree until leaf level
          while c > 1:
            w = self.__ix(sentence, i-c)
            ch = ch.setdefault(w, {})
            c -= 1
          # on leaf level, add the word
          w = self.__ix(sentence, i-1)
          ch.setdefault(w, []).append(word)
    return None


  def linearize(self, sentence):
    return self.__delimiter.join(sentence)


  # check if a string is a verbatim part of an exiting tweet
  def __is_sublist(self, haystack, needle):
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


  # jump back a random distance
  def __backjump(self, sentence):
    n = len(sentence)
    c = random.randint(0, n)
    return sentence[0:c]


  # generate a tweet based on the n-gram chains
  def generate(self, maxlen):

    sentence = []
    while True:

      try:
        ngram = random.choice(self.__odds)
        choices = self.__chains[ngram]

        # go through chain tree according to previous words
        while ngram:
          i = len(sentence) - ngram
          w = self.__ix(sentence, i)
          choices = choices[w]
          ngram -= 1

      except KeyError:
        choices = []

      if not choices:
        # no way forward, let's go back
        sentence = self.__backjump(sentence)
        continue

      word = random.choice(choices)

      if not word:
        break # False: end of sentence

      else:
        sentence.append(word)
        # it's too long, let's go back
        if len(self.linearize(sentence)) >= maxlen:
          sentence = self.__backjump(sentence)

    return sentence


  def generate_with_checks(self, maxlen):
    blacklist = self.__corpus + self.__backlog
    while True:
      output = self.generate(maxlen)
      # leave when it's not a repeat
      if not self.__is_sublist(blacklist, output):
        break
      print(":(", output)
    return output
