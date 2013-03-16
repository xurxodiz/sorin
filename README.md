Sorin
=====

Sorin is a bunch of scripts bundled together that download tweets, parse them into a JSON dictionary, produce random tweets out of it following Markov chain conventions, and then tweet them.

You can see it at work on [@MarkovUnchained](http://twitter.com/MarkovUnchained).


How it works
=====

The tweets are split into words, then those words are stored according to what words follow what words. Then, a word is picked at random, and among all the possible words that have been found to follow it, one is picked at random according to is frequency. Repeat until the word picked can end a sentence. If you exceed tweet size, the last word will be discarded and a new one will be chosen. If there are no possible ways forward, yet another word is dropped and paths are searched from there.


How to use it
=====

Run `make init ACCOUNT=name_of_the_account` to create the folders and download the first batch of tweets from that user.

(you should run `make fetch ACCOUNT=name_of_the_account` periodically afterwards to get the new tweets since last time)

Then, run `make parse ACCOUNT=name_of_the_account` to create the dictionary (the first time you run the init script this will be done for you automatically).

`make generate ACCOUNT=name_of_the_account` will create the tweets and print them on screen.

If you create a `SECRET` file with your Twitter consumer key, consumer secret, access key, and access token in different lines, inside of the `scripts` folder, you can run `make tweet ACCOUNT=name_of_the_account` to both generate and automatically post them. You'll see them displayed on screen as well.