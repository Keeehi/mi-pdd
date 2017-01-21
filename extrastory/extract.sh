#!/bin/bash

for PAGE in {1..140}
do
    sed -e '/card_headline/,/>/!d' html/es.$PAGE.html | grep -vE "</?div" | cut -c13- >> es.all.txt
done
