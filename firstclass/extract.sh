#!/bin/bash

for PAGE in {1..396}
do
    sed -n -e 's/ *<meta.*itemprop="headline " content="//p' html/fc.$PAGE.html | sed -n -e 's/"><meta.*>//p' >> fc.all.txt
done
