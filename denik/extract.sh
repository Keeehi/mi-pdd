#!/bin/bash

for PAGE in {1..1000}
do
    grep "<h2>" html/d.$PAGE.html | sed -n -e 's/\s*<h2><a.*href="[^>]*">//p' | sed -n -e 's/<\/a>//p' >> d.all.txt
done
