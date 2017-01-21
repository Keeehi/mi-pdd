#!/usr/bin/python3
import re
import unicodedata
import sys
from Stemmer import Stemmer

stemmer = Stemmer()

def preprocessor(s):
    words = []
    for word in re.compile(r'[\w\-]+').findall(s):
        words.append(stemmer.stem(word))

    nkfd_form = unicodedata.normalize('NFKD', ' '.join(words).lower())
    return nkfd_form.encode('ASCII', 'ignore').decode('ASCII')


print("Processing ...")
for filename in sys.argv[1:]:
    print("  FILE " + filename)
    try:
        with open(filename) as file:
            processed_lines = []
            lines = file.read().split('\n')
            print("    Total lines " + str(len(lines)))
            for index, line in enumerate(lines):
                processed_lines.append(preprocessor(line))

                if (index + 1) % 5 == 0:
                    print("      " + str((index+1)*100/len(lines)) + "%")

        with open(filename, mode='w') as file:
            file.write("\n".join(processed_lines))

    except FileNotFoundError:
        print("  SKIPPING " + filename + " because it does not exist.")
print("done")
