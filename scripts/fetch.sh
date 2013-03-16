#!/bin/sh

SUBJECT=$1

ID=$(cat archive/$SUBJECT/id) 
scripts/fetch.py $SUBJECT $ID > archive/$SUBJECT/tmp
scripts/append.sh $SUBJECT