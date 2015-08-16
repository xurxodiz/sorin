Sorin
=====

Sorin is a bunch of scripts bundled together that reads sentences, parse them into a JSON dictionary, produce random sentences out of them following Markov chain conventions, and then tweet them.

It started with tweets, but it has been expanded to work with lyrics, prose and theatrical scripts.

You can see it at work on [@MarkovUnchained](http://twitter.com/MarkovUnchained).

Please keep in mind that sorin is developed under OSX, so even if I try to be Linux-compliant, I can't guarantee full compatibility (the tweaking needed, in any case, should be quite minor).


How it works
=====

The sentences are split into words, then those words are stored according to what words follow what words. Then, a word is picked at random, and among all the possible words that have been found to follow it, one is picked also at random according to is frequency. Repeat until the word picked can end a sentence. If it exceeds 140 characters, a tail chunk of the sentence is discarded at random and a words are picked again from the cutpoint. This process is done until a suitable sentence is formed.

To pick a word, the algorithm uses frequency based on either just the previous word, or the two previous words (with a 1/3 and 2/3 probability respectively). For more details, search information on "Markov chains" or read the code.

After a sentence is generated, it is checked that it is not neither an exact duplicate of an existing source sentence, nor an exact subpart of an existing source sentence, nor a repeat of a sentence that was generated before. In any of those cases, the sentence is wholly discarded and the process is started anew. If it is good to go, the generated sentence is appended to the log of past generated sentences. See further below on how to clear it (*How to use it*)


### Sentence postprocessing

(most of this would only applied to tweets, but it is done to all source sentences anyway)

All URLs are removed, as well as initial "RT" prefixes, and any colons found right before a URL. @-Mentions in the middle of the text are fine, but they are removed if at the beggining of the sentence. This (done already in subtask `make depure`) is so texts tweeted by the algorithm are never output as direct replies, and can be viewed by everybody.

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

Lyrics are expected to alredy be cut in sentences (one per line).


For prose
----------

Place each text in a txt inside `prose/name_of_the_author`. Do not use spaces in the name of the author. It's safe to use them in filenames for each text though.

Then, run `make init-prose ACCOUNT=name_of_the_author` to automatically create the folder inside `archive` and the needed files.

Texts might be composed in paragraphs and include dialog. They will be cut into sentences.


For theatrical scripts
-------------

For each show (film, series...) create a folder inside `theatre/name_of_show`. You can then place the script in PDF format inside that folder if it's a film, or create folders for seasons and then the script for each episode inside them if it's a series. Whatever is better for you.

Inside the `name_of_show` folder you need a text file called simply `characters` with each line holding the name of a character you want to extract. It needs to be uppercase if the characters' name are uppercase in the script (as they usually are).

Now, run `make init-theatre SHOW=name_of_the_show` to automatically extract each character's sentences inside a `name_of_show-name_of_character` folder in `archive`. This `name_of_show-name_of_character` construct is the name of the account you will need to use for generating sentences (see below).


How to use it
======

`make generate ACCOUNT=name_of_the_account` will create the sentences and print them on screen.

You can run `make tweet ACCOUNT=name_of_the_account` to both generate and automatically tweet the sentences. You'll see them displayed on screen as well.

`make clean-past` clears the log of past generated sentences, (see above in *How it works* for more info on the checks performed).
