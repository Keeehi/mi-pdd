#!/bin/bash

for PAGE in {1..258}
do
    sed -e '/views-field-title/,/>/!d' html/ip.$PAGE.html | grep field-content | sed -n -e 's/<div class="field-content"><a href=".*">//p' | sed -n -e 's/<\/a><\/div>//p' | head -20 >> ip.all-temp.txt
done

head -n -4 ip.all-temp.txt > ip.all.txt
rm ip.all-temp.txt
