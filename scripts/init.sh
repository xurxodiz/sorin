#!/bin/sh

SUBJECT=$1

mkdir -p archive/$SUBJECT/
scripts/init.py $SUBJECT > archive/$SUBJECT/tmp
scripts/append.sh $SUBJECT