#!/bin/bash

for PAGE in {1..240}
do
    sed -e '/postList /,/<script type="text\/javascript">CiliChili/!d' html/cc.$PAGE.html | tr '\n' ' ' | sed 's/<h3>/\n/g' | sed -n -e 's/<a[^>]*>//p' | sed -n -e 's/<\/a>.*//p' | tail -n +2 >> cc.all.txt
done
