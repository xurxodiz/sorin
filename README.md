Sorin
=====

Sorin is a bunch of scripts bundled together that download tweets, parse them into a JSON dictionary, produce random tweets out of it following Markov chain conventions, and then tweet them.

It as been expanded to work with lyrics and prose text too, after some cooking.

You can see it at work on [@MarkovUnchained](http://twitter.com/MarkovUnchained).

Please keep in mind that sorin is developed for use on OSX, therefore some tweaking might be needing for full compatibility on other UNIXes.


How it works
=====

The tweets are split into words, then those words are stored according to what words follow what words. Then, a word is picked at random, and among all the possible words that have been found to follow it, one is picked at random according to is frequency. Repeat until the word picked can end a sentence. If you exceed tweet size, the last word will be discarded and a new one will be chosen. If there are no possible ways forward, yet another word is dropped and paths are searched from there.

The new iteration of the algorithm uses either just the previous word, or the two previous words (with a 1/3 and 2/3 probability respectively), as basis to determine the following word.

After a tweet is generated, it is checked that it is not neither an exact duplicate of an existing tweet, nor an exact subpart of an existing tweet, nor a repeat of a tweet that was generated before. In any of those cases, the tweet is wholly discarded and the process is started anew. If it is good to go, the generated tweet is appended to the log of past generated tweets. See further below on how to clear it (*How to use it*)


### Tweet postprocessing

All URLs are removed from tweets, as well as initial "RT" prefixes, and any colons found right before a URL. Mentions in the middle of the text are fine, but they are removed if at the beggining of the tweet. This (done already in subtask `make depure`) is so texts tweeted by the algorithm are never output as direct replies, and can be viewed by everybody.

Also, brackets and quotation marks of all kinds are removed, as well as opening ¿ and ¡ signs.


Setup
=====

You'll need Python2 and the [python-twitter](https://github.com/bear/python-twitter) library–--the reason why some parts are still stuck at it---but also Python3 (unicode string handling is much smoother with it). `init`, `fetch` and `tweet` scripts use Python2, while `parse` and `generate` use Python3.

You must create a `SECRET` file with your Twitter consumer key, consumer secret, access key, and access token in different lines, inside of the `scripts` folder.

For tweets
----------

Run `make init ACCOUNT=name_of_the_account` to create the folders and download the first batch of tweets from a user.

(you should run `make fetch ACCOUNT=name_of_the_account` periodically afterwards to get the new tweets since last time, or `make update` to update them all)

For lyrics
----------

Place each song's lyrics in a txt inside `lyrics/name_of_the_band`. Do not use spaces in the name of the band. It's safe to use them in filenames for each song though.

Then, run `make init-lyrics ACCOUNT=name_of_the_band` to automatically create the folder inside `archive` and the needed files.

Lyrics are expected to alredy be cut in sentences (one per line), as if they were tweets.

For prose
----------

Place each text in a txt inside `prose/name_of_the_author`. Do not use spaces in the name of the author. It's safe to use them in filenames for each text though.

Then, run `make init-prose ACCOUNT=name_of_the_author` to automatically create the folder inside `archive` and the needed files.

Texts might be composed in paragraphs and include dialog. They will be cut into sentences.


How to use it
======

`make generate ACCOUNT=name_of_the_account_band_or_author` will create the tweets and print them on screen.

You can run `make tweet ACCOUNT=name_of_the_account_or_band` to both generate and automatically post tweets. You'll see them displayed on screen as well.

`make clean-past` clears the log of past generated tweets, (see above in *How it works* for more info on the checks performed).
