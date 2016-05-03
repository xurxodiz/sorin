Sorin
=====

Sorin is a bunch of scripts bundled together that read sentences, parse them into a JSON dictionary, produce random sentences out of them following Markov chain conventions, and then tweet them.

It started with tweets, but it has been expanded to work with lyrics, prose and theatrical scripts.

You can see it at work on [@MarkovUnchained](http://twitter.com/MarkovUnchained).

Please keep in mind that sorin is developed under OSX, so even if I try to be Linux-compliant, I can't guarantee full compatibility (the tweaking needed, in any case, should be quite minor).


How it works
=====

The sentences are split into words, then those words are stored according to what words follow what words. To start, a word is picked amongst those that have been found to begin a sentence, and then another one is picked amongst those that could follow it. Repeat until the next word picked is the end of sentence mark. If the sentence exceeds 140 characters, an arbitrary tail chunk of the sentence is discarded and words are picked again from the cutpoint. This process is done until a suitable sentence is formed.

To pick a word, the algorithm uses frequency based on either just the previous word, or the two previous words (with a 1/3 and 2/3 probability respectively). For more details, search information on Markov chains or read the code.

After a sentence is generated, it is checked that it is neither an exact duplicate of an existing source sentence, nor an exact subpart of an existing source sentence, nor a repeat of a sentence that was generated before. In any of those cases, the sentence is wholly discarded and the process is started anew. If it is good to go, the generated sentence is appended to the log of past generated sentences. See further below on how to clear it (*How to use it*)


### Source sentence postprocessing

All URLs are removed, as well as preceeding colons if any, and a period is placed instead--unless the previous sentence already had it (or a ! or ?).

Brackets and quotation marks of all kinds are removed, as well as opening ¿ and ¡ signs.

Please note that when fetching tweets, both retweets and direct replies are explicitly not requested.

Requisites
=====

You need Python3 and Perl.

If you want to `init` or `fetch` from Twitter, or `tweet`, you need the [Python Twitter Tools](https://github.com/sixohsix/twitter) as well. You must also create a `SECRET` text file with your Twitter access token key, access token, consumer key and consumer secret in different lines (in this order) inside of the `scripts` folder.

To `init-theatre` you need the `pdftotext` utility. You can get it from the `xpdf` package: on Linux use your favourite package manager, and on OSX just `brew tap homebrew/x11` and `brew install xpdf`.


For tweets
----------

Run `make init-twitter ACCOUNT=name_of_the_account` to create the folders and download the first batch of tweets from a user.

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

For each show (film, series...) create a folder inside `theatre/name_of_show` (do not use spaces in the name of the show). You can then place the script in PDF format inside that folder if it's a film, or create folders for seasons and then the script for each episode inside them if it's a series. Whatever is better for you.

Inside the `name_of_show` folder you need a text file called simply `characters` with each line holding the name of a character you want to extract. It needs to be uppercase if the characters' names are uppercase in the script (as they usually are).

Now, run `make init-theatre SHOW=name_of_the_show` to automatically extract each character's sentences inside a `name_of_show-name_of_character` folder in `archive`. This `name_of_show-name_of_character` construct is the name of the account you will need to use for generating sentences (see below).


How to use it
======

`make generate ACCOUNT=name_of_the_account` will create the sentences and print them on screen.

You can run `make tweet ACCOUNT=name_of_the_account` to both generate and automatically tweet the sentences. You'll see them displayed on screen as well.

`make clean-past` clears the log of past generated sentences (see above in *How it works* for more info on the checks performed).
