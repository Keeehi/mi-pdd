#!/bin/bash

for PAGE in {1..1000}
do
#    sed -n -e 's/<\/a><\/div>//p' ip-e.$PAGE.html | head -20 >> ip.all.txt
#    sed -n -e 's/<div class="field-content"><a href=".*">//p' ip-e2.$PAGE.html > ip-e.$PAGE.html
#    grep field-content ip-e.$PAGE.html > ip-e2.$PAGE.html
#    sed -e '/views-field-title/,/>/!d' ip.$PAGE.html > ip-e.$PAGE.html
    wget http://www.lidovky.cz/zpravy-domov.aspx?strana=$PAGE -nv -O lidovky/html/l.$PAGE.html
done
