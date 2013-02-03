Sorin
=====

Sorin is a bunch of scripts bundled together that download tweets, parse them into a JSON dictionary, produce random tweets out of it following Markov chain conventions, and then tweet them.

You can see it at work on [@MarkovUnchained](http://twitter.com/MarkovUnchained).


How it works
=====

The tweets are split into words, then those words are stored according to what words follow what words. Then, a word is picked at random, and among all the possible words that have been found to follow it, one is picked at random according to is frequency. Repeat until the word picked can end a sentence or you get a long enough string.


How to use it
=====

Run `./init.sh USERNAME` to create the folders and download the first batch of tweets from that user.

(you should run `./fetch.sh USERNAME` periodically afterwards to get the new tweets since last time)

Then, run `./parse.py USERNAME` to create the dictionary.

`./generate.py USERNAME` will create the tweets and print them on screen.

If you create a `SECRET` file with your Twitter consumer key, consumer secret, access key, and access token in different lines, you can run `./tweet.py` TWEET to post them.

Use `./generate.py USERNAME | ./tweet.py` to do both at the same time.