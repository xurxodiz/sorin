#!/bin/sh

SUBJECT=$1

sed -i '' 's!\http\(s\)\{0,1\}://[^[:space:]]*!!g' archive/$SUBJECT/tmp
head -n 1 archive/$SUBJECT/tmp > archive/$SUBJECT/id
tail -n +2 archive/$SUBJECT/tmp >> archive/$SUBJECT/log
awk '!x[$0]++' <archive/$SUBJECT/log >archive/$SUBJECT/tmp
sed '/^$/d' <archive/$SUBJECT/tmp >archive/$SUBJECT/log
rm archive/$SUBJECT/tmp
scripts/parse.py $SUBJECT