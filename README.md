Sorin
=====

Sorin is a bundle of scripts for making Markov chains. It started with tweets, but it has been expanded to work with lyrics, prose and theatrical scripts, and has spawned a command line utility that rocks.

You can see a demo at work on [@MarkovUnchained](http://twitter.com/MarkovUnchained).

Please keep in mind that the sorin Makefiles are developed under OSX, so even if I try to be Linux-compliant, I can't guarantee full compatibility (the tweaking needed, in any case, should be quite minor).

The command line utility
=====

This is the cool part now. It can read the corpus from a file or by piping into it. It will generate the necessary internal dictionaries on the fly, or load them from a file (and saving them if you want). You can specify the delimiters that separate the sentences and the tokens inside them. You can fix a maximum length of the generated strings and ask it to generate more than one chain each time. It will check that the production is not a repeat of the corpus or of a previous backlog in some file. And you can tell the ngram usage according to a list of odds.

Best way to check all parameters is to `scripts/markov -h`, but here are some examples.

Let's say we have a list of numbers and we want to generate a chain based on them:

    $ echo -n "87964_467709_386_50876_4489076" | scripts/markov -x "_" -d ""
    509

(note the `-n` in the `echo` to avoid that pesky trailing newline)

We use `-x` for the sentence delimiter and `-d` for the token delimiter. Now, the result is a bit short, so we can set a minimum and maximum length as well with `-m` and `-M`:

    $ echo -n "87964_467709_386_50876_4489076" | scripts/markov -d "" -x "_" -m 7 -M 9
    48909676

This way we get a number with between 7 and 9 digits (both included).

If you get your hands on a big list of words, you can have fun creating words as well. Words are a bit heavier, so let's save time by saving our internal dictionaries:

    $ cat dict.txt | scripts/markov -s dict.json -d "" -o 2 3 -n 0

We use `-s` to name the output file and `-o` to ask for 2 and 3-grams. Again, the token delimiter (`-d`) is going to be empty, since each character will be its own token. Finally, since we don't want it to generate anything at this moment (zero output), we set `-n` to 0.

In these cases, more often than not, it's more convenient to load the corpus from a file with `-c`:

    $ scripts/markov -c dict.txt -s dict.json -d "" -o 2 3 -n 0

In any case, now we can use this dict to generate our words!

    $ scripts/markov -l dict.json -d "" -n 3
    enviar
    guridupiése
    ransador

The dictionary is loaded with `-l` and the number of productions wanted with `-n` as before. Note we need to set the token delimiter again with `-d`, because it's used to *glue* together the tokens in the output.

But, what's this? **enviar** is already a word! That's not fun. To check that the output is always new (not in the source corpus), pass the `-k` flag:

    $ cat dict.txt | scripts/markov -l dict.json -d "" -k
    conalsaprota

Or, with the `-c` flag for corpus:

    $ scripts/markov -c dict.txt -l dict.json -d "" -k
    conalsaprota

Much better :)

If you want to play with the odds of using each of the ngrams present in the dictionary, you can do it again with the `-o`option:

    $ cat dict.txt | scripts/markov -l dict.json -d "" -o 2 3 3 -k
    bilihuilla

With this above command, for each letter it chooses it will do so 66% of the time based on 3-grams, and 33% of the time based on 2-grams.

Finally, if you keep your corpus saved on disk, along with the generated dictionaries and a backlog of previously generated funsies, you can use them all like so:

    $ scripts/markov -c corpus.txt -l dict.json -b backlog.txt -k

This will produce output based on the loaded dictionary (`-l`), and check (`-k`) that none of the results are found on the corpus (`-c`) or the backlog (`-b`). As any time that the odds are not passed as parameters, it will use those ngrams with which the dictionary was built as the ones to use, balanced equally.


Go and have fun! My recommendation is to symlink the script from `/usr/local/bin` or put it somewhere else in your `PATH`, etc.


What's not the CL utility
=====

The rest of the repository is a couple Python scripts that work with the same codebase as the utility and some Makefile magic (with some Perl) to interface with Twitter and tie everything together. The rest of this README will refer to the default behaviour for this wrapping framework, and **NOT** the CL.


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

  