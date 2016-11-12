#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from Markov import Markov


if __name__ == "__main__":

  corpuspath = "archive/"+sys.argv[1]+"/log"
  chainpath = "archive/"+sys.argv[1]+"/json"

  m = Markov(corpusFile=corpuspath)
  m.save_chains(chainpath)
