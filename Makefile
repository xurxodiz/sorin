init:
	@mkdir -p archive/$(ACCOUNT)/
	@scripts/init.py $(ACCOUNT) > archive/$(ACCOUNT)/tmp2
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

fetch:
	@if [ -f archive/$(ACCOUNT)/id ]; then \
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

update:
	@$(foreach ACC,$(patsubst archive/%,%,$(wildcard archive/*)),make fetch ACCOUNT=$(ACC);)

depure:
	@# remove links
	@perl -pi -e 's!https?://[^\s]*!!g' archive/$(ACCOUNT)/tmp
	@# remove manual RTs
	@perl -i -ne 'print unless /^RT @/' archive/$(ACCOUNT)/tmp
	@# remove mentions on replies
	@perl -pi -e 's/^(@[[:alnum:]_]+ )+//' archive/$(ACCOUNT)/tmp
	@# remove duplicate lines
	@awk '!x[$$0]++' <archive/$(ACCOUNT)/tmp >archive/$(ACCOUNT)/tmp2
	@# remove empty lines
	@perl -n -e 'print unless /^$$/' <archive/$(ACCOUNT)/tmp2 >archive/$(ACCOUNT)/log
	@rm archive/$(ACCOUNT)/tmp
	@rm archive/$(ACCOUNT)/tmp2

generate:
	@scripts/generate.py $(ACCOUNT)

parse:
	@scripts/parse.py $(ACCOUNT)

tweet:
	@make generate ACCOUNT=$(ACCOUNT) --no-print-directory | scripts/tweet.py
