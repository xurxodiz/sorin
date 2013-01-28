#!/bin/sh

SUBJECT=$1
DIRECTION=$2

ID=$(cat archive/$SUBJECT/$(echo $DIRECTION)_id) 
./fetch.py $SUBJECT $DIRECTION $ID > archive/$SUBJECT/tmp
sed -i '' 's!\http\(s\)\{0,1\}://[^[:space:]]*!!g' archive/$SUBJECT/tmp
head -n 1 archive/$SUBJECT/tmp > archive/$SUBJECT/$(echo $DIRECTION)_id
if [[ $DIRECTION == "back" ]]; then
	tail -n +2 archive/$SUBJECT/tmp >> archive/$SUBJECT/log
	rm archive/$SUBJECT/tmp
else
	tail -n +2 archive/$SUBJECT/tmp >> archive/$SUBJECT/aux
	cat archive/$SUBJECT/log >> archive/$SUBJECT/aux
	rm archive/$SUBJECT/log archive/$SUBJECT/tmp
	mv archive/$SUBJECT/aux archive/$SUBJECT/log
fi

sed -i '' '/^$/d' archive/$SUBJECT/log
