#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import xml.sax.saxutils

from Markov import Markov


if __name__ == "__main__":

  chainpath = "archive/"+sys.argv[1]+"/json"
  corpuspath = "archive/"+sys.argv[1]+"/log"
  backlogpath = "archive/"+sys.argv[1]+"/past"

  m = Markov(corpusFile=corpuspath, chainsFile=chainpath, backlogFile=backlogpath, odds=[1, 2, 2, 3])
  m.save_chains(chainpath)
  output = m.generate_with_checks(140)

  # we leave ! and ? since they make sense isolated
  output = [w.translate(str.maketrans('', '', '"()[]{}«»¡¿')) for w in output]
  output = m.linearize(output)
  output = xml.sax.saxutils.unescape(output)

  print(output)

  with open("archive/"+sys.argv[1]+"/past", 'a+') as f:
    f.write(output+"\n")
