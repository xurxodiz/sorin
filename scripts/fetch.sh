#!/bin/sh

SUBJECT=$1

ID=$(cat archive/$SUBJECT/id) 
scripts/fetch.py $SUBJECT $ID > archive/$SUBJECT/tmp
sed -i '' 's!\http\(s\)\{0,1\}://[^[:space:]]*!!g' archive/$SUBJECT/tmp
head -n 1 archive/$SUBJECT/tmp > archive/$SUBJECT/id
tail -n +2 archive/$SUBJECT/tmp >> archive/$SUBJECT/log
rm archive/$SUBJECT/tmp
sed -i '' '/^$/d' archive/$SUBJECT/log