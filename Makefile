init:
	@mkdir -p archive/$(ACCOUNT)/
	@scripts/init.py $(ACCOUNT) > archive/$(ACCOUNT)/tmp
	@make append ACCOUNT=$(ACCOUNT)

fetch:
	@$(eval ID:=$(shell cat archive/$(ACCOUNT)/id))
	@scripts/fetch.py $(ACCOUNT) $(ID) >archive/$(ACCOUNT)/tmp
	@make append ACCOUNT=$(ACCOUNT)

append:
	@sed -i '' 's!\http\(s\)\{0,1\}://[^[:space:]]*!!g' archive/$(ACCOUNT)/tmp
	@sed -E -i '' 's/^(RT )*(@[[:alpha:]_]+ )*//' archive/$(ACCOUNT)/tmp
	@head -n 1 archive/$(ACCOUNT)/tmp > archive/$(ACCOUNT)/id
	@tail -n +2 archive/$(ACCOUNT)/tmp >> archive/$(ACCOUNT)/log
	@awk '!x[$$0]++' <archive/$(ACCOUNT)/log >archive/$(ACCOUNT)/tmp
	@sed '/^$$/d' <archive/$(ACCOUNT)/tmp >archive/$(ACCOUNT)/log
	@rm archive/$(ACCOUNT)/tmp
	@make parse ACCOUNT=$(ACCOUNT)

generate:
	@scripts/generate.py $(ACCOUNT)

parse:
	@scripts/parse.py $(ACCOUNT)

tweet:
	@scripts/tweet.py "`make generate ACCOUNT=$(ACCOUNT)`"