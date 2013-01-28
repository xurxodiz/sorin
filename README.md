Sorin
=====

Sorin is a bunch of scripts bundled together that download tweets, parse them into a JSON dictionary, produce random tweets out of it following Markov chain conventions, and then tweet them.

You can see it at work on @MarkovUnchained.


How it works
=====

The tweets are split into words, then those words are stored according to what words follow what words. Then, a word is picked at random, and among all the possible words that have been found to follow it, one is picked at random according to is frequency. Repeat until the word picked can end a sentence or you get a long enough string.


How to use it
=====

You need to create an `archive` folder and inside it, a folder named as the Twitter user that you want to parse.

In that user's folder, create two text files, `back_id` and `forth_id`, with the number of a tweet from that user.

Run `./fetch.sh USERNAME back` to fill the log with tweets from `back_id` to before in time.

Run `./fetch.sh USERNAME forth` to fill the log with tweets from `forth_id` to afterwards in time.

Once the log is sufficiently full, run `./parse.py USERNAME` to create the dictionary.

`./generate.py USERNAME` will create the tweets and print them on screen.

If you create a `SECRET` file with your Twitter consumer key, consumer secret, access key, and access token in different lines, you can run `./tweet.py` TWEET to post them.

Use `./generate.py USERNAME | ./tweet.py` to do both at the same time.