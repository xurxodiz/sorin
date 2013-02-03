#!/bin/sh

SUBJECT=$1

mkdir -p archive/$SUBJECT/
scripts/init.py $SUBJECT > archive/$SUBJECT/tmp
sed -i '' 's!\http\(s\)\{0,1\}://[^[:space:]]*!!g' archive/$SUBJECT/tmp
head -n 1 archive/$SUBJECT/tmp > archive/$SUBJECT/id
tail -n +2 archive/$SUBJECT/tmp >> archive/$SUBJECT/log
rm archive/$SUBJECT/tmp
sed -i '' '/^$/d' archive/$SUBJECT/log