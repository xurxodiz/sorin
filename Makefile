init:
	@mkdir -p archive/$(ACCOUNT)/
	@scripts/init.py $(ACCOUNT) > archive/$(ACCOUNT)/tmp
	@make depure ACCOUNT=$(ACCOUNT)
	@make parse ACCOUNT=$(ACCOUNT)

init-lyrics:
	@mkdir -p archive/$(ACCOUNT)/
	@cat lyrics/$(ACCOUNT)/*.txt > archive/$(ACCOUNT)/tmp
	@make depure ACCOUNT=$(ACCOUNT)
	@make parse ACCOUNT=$(ACCOUNT)

fetch:
	@$(eval ID:=$(shell cat archive/$(ACCOUNT)/id))
	@scripts/fetch.py $(ACCOUNT) $(ID) >archive/$(ACCOUNT)/tmp2
	@head -n 1 archive/$(ACCOUNT)/tmp2 > archive/$(ACCOUNT)/id
	@tail -n +2 archive/$(ACCOUNT)/tmp2 >> archive/$(ACCOUNT)/tmp
	@make depure ACCOUNT=$(ACCOUNT)
	@make parse ACCOUNT=$(ACCOUNT)

update:
	@$(foreach ACC,$(patsubst archive/%,%,$(wildcard archive/*)),make fetch ACCOUNT=$(ACC);)

depure:
	@# remove links
	@sed -i '' 's!http\(s\)\{0,1\}://[^[:space:]]*!!g' archive/$(ACCOUNT)/tmp
	@# remove manual RTs
	@sed -E -i '' '/^RT @/d' archive/$(ACCOUNT)/tmp
	@# remove mentions on replies
	@sed -E -i '' 's/^(@[[:alnum:]_]+ )+//' archive/$(ACCOUNT)/tmp
	@# remove duplicate lines
	@awk '!x[$$0]++' <archive/$(ACCOUNT)/tmp >archive/$(ACCOUNT)/tmp2
	@# remove empty lines
	@sed '/^$$/d' <archive/$(ACCOUNT)/tmp2 >archive/$(ACCOUNT)/log
	@rm archive/$(ACCOUNT)/tmp
	@rm archive/$(ACCOUNT)/tmp2

generate:
	@scripts/generate.py $(ACCOUNT)

parse:
	@scripts/parse.py $(ACCOUNT)

tweet:
	@make generate ACCOUNT=$(ACCOUNT) --no-print-directory | scripts/tweet.py
