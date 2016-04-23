init-twitter:
	@mkdir -p archive/$(ACCOUNT)/
	@scripts/init-twitter.py $(ACCOUNT) > archive/$(ACCOUNT)/tmp2
	@make split ACCOUNT=$(ACCOUNT)
	@make depure ACCOUNT=$(ACCOUNT)
	@make parse ACCOUNT=$(ACCOUNT)

init-lyrics:
	@mkdir -p archive/$(ACCOUNT)/
	@cat lyrics/$(ACCOUNT)/*.txt > archive/$(ACCOUNT)/tmp
	@make depure ACCOUNT=$(ACCOUNT)
	@make parse ACCOUNT=$(ACCOUNT)

init-prose:
	@# spaces and bash don't play well, copy swapping them for _
	@$(shell cd prose/$(ACCOUNT)/ && mkdir -p tmp && pax -wrs'/ /_/g' *txt tmp/)
	@$(foreach FILE,$(wildcard prose/$(ACCOUNT)/tmp/*),make prepare-prose FILE=$(FILE);)
	@mkdir -p archive/$(ACCOUNT)/
	@cat prose/$(ACCOUNT)/tmp/*.txt > archive/$(ACCOUNT)/tmp
	@rm -rf prose/$(ACCOUNT)/tmp
	@make depure ACCOUNT=$(ACCOUNT)
	@make parse ACCOUNT=$(ACCOUNT)

prepare-prose:
	@# first remove trailing whitespace
	@perl -pli -Mutf8 -CSAD -e 's/\s*$$//g' $(FILE)
	@# A) Then the boy said:
	@# B) Then the boy said.
	@perl -pi -Mutf8 -CSAD -e 's/:\n/.\n/g' $(FILE)
	@# A) Yikes! Why?
	@# B) Yikes! \n Why ?
	@perl -pi -Mutf8 -CSAD -e 's/([.!?]["»]?) ([[:upper:]¡¿"»«])/\1\n\2/g' $(FILE)
	@# A) Weird as it might be \n this is not a haiku
	@# B) Weird as it might be this is not a haiku
	@perl -pi -Mutf8 -CSAD -e 's|([^.!?»])\s*\n+\s*|\1 |g' $(FILE)

init-theatre:
	@$(foreach FILE,$(wildcard theatre/$(SHOW)/*.pdf theatre/$(SHOW)/*/*.pdf),make prepare-theatre FILE=$(FILE);)
	@$(eval CHARACTERS:=$(shell cat theatre/$(SHOW)/characters))
	@$(foreach CHARACTER,$(CHARACTERS),make prepare-theatre-character SHOW=$(SHOW) CHARACTER=$(CHARACTER);)
	@(cd theatre/$(SHOW) && find . -name "*.txt" -type f -delete)

prepare-theatre:
	@# using -layout might improve results, but it needs more work for a multiline match
	@pdftotext -enc UTF-8 -eol unix -nopgbrk $(FILE) $(FILE).txt
	@perl -pi -Mutf8 -CSAD -e 's/[^[:print:]\n]//' $(FILE).txt

prepare-theatre-character:
	@$(eval ACCOUNT:=$(shell echo $(SHOW)-$(CHARACTER) | tr " " "_"))
	@mkdir -p archive/$(ACCOUNT)
	@(cd theatre/$(SHOW) && find . -name "*.txt" -print0 | xargs -0 cat) > archive/$(ACCOUNT)/tmp
	@perl -ni -Mutf8 -CSAD -e 's/^$(CHARACTER) ([A-Z])/\1/ && print' archive/$(ACCOUNT)/tmp
	@perl -pi -Mutf8 -CSAD -e 's/\s+\([^)]+\)\s+/ /' archive/$(ACCOUNT)/tmp
	@make depure ACCOUNT=$(ACCOUNT)
	@make parse ACCOUNT=$(ACCOUNT)

fetch:
	@if [ -f archive/$(ACCOUNT)/id ]; then \
		echo "Fetching $(ACCOUNT)..."; \
		make fetch-work ACCOUNT=$(ACCOUNT); \
	fi

fetch-work:
	@# read id of last tweet saved, and fetch more
	@$(eval ID:=$(shell cat archive/$(ACCOUNT)/id))
	@scripts/fetch.py $(ACCOUNT) $(ID) >archive/$(ACCOUNT)/tmp2
	@make split ACCOUNT=$(ACCOUNT)
	@make depure ACCOUNT=$(ACCOUNT)
	@make parse ACCOUNT=$(ACCOUNT)

split:
	@# first line output is new id of last tweet
	@head -n 1 archive/$(ACCOUNT)/tmp2 > archive/$(ACCOUNT)/id
	@# the rest is the the log of new tweets fetched
	@tail -n +2 archive/$(ACCOUNT)/tmp2 >> archive/$(ACCOUNT)/tmp
	@# we won't need tmp2 anymore
	@rm archive/$(ACCOUNT)/tmp2

update:
	@$(foreach ACC,$(patsubst archive/%,%,$(wildcard archive/*)),make fetch ACCOUNT=$(ACC);)

clean-past:
	@$(foreach ACC,$(patsubst archive/%,%,$(wildcard archive/*)),rm -rf archive/$(ACC)/past;)

depure:
	@# remove links
	@perl -pi -e 's!(: )?https?:/[^\s]+!. !g' archive/$(ACCOUNT)/tmp
	@# prevent error line below
	@touch archive/$(ACCOUNT)/log
	@# construct new joined file
	@cat archive/$(ACCOUNT)/log archive/$(ACCOUNT)/tmp >archive/$(ACCOUNT)/tmp2
	@# remove empty lines
	@perl -i -ne 'print unless /^\s*$$/' archive/$(ACCOUNT)/tmp2
	@# remove possible duplicated lines (eg twitter fetch overlap)
	@awk '!x[$$0]++' <archive/$(ACCOUNT)/tmp2 >archive/$(ACCOUNT)/tmp3
	@# cleanup
	@rm archive/$(ACCOUNT)/tmp
	@rm archive/$(ACCOUNT)/tmp2
	@# we don't overwrite log until the very end to prevent screwups
	@mv archive/$(ACCOUNT)/tmp3 archive/$(ACCOUNT)/log

generate:
	@scripts/generate.py $(ACCOUNT)

parse:
	@scripts/parse.py $(ACCOUNT)

tweet:
	@$(eval TWEET:=$(shell make generate ACCOUNT=$(ACCOUNT) --no-print-directory))
	@if [ "x" != "x$(TWEET)" ]; then \
	  scripts/tweet.py "$(TWEET)"; \
	fi
