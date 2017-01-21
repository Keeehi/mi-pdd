#!/bin/bash

for PAGE in {1..1206}
do
    sed -n -e 's/.*<h2><a href="[^>]*">//p' html/g.$PAGE.html | sed -n -e 's/<\/a>.*//p' >> g.all.txt
done
