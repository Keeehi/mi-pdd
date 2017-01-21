#!/usr/bin/python3
import io
import os
import sys
import re
import unicodedata
from sklearn import linear_model
from sklearn.feature_extraction.text import TfidfVectorizer
from Stemmer import Stemmer

stemmer = Stemmer()


def preprocessor(s):
    words = []
    for word in re.compile(r'[\w\-]+').findall(s):
        words.append(stemmer.stem(word))

    nkfd_form = unicodedata.normalize('NFKD', ' '.join(words).lower())
    return nkfd_form.encode('ASCII', 'ignore').decode('ASCII')


stop_words = []
stop_words_filename = 'czech_stop_words/combined.txt'
print('Loading stop words')
if os.path.isfile(stop_words_filename[:-4] + '.stemmed.txt'):
    with open(stop_words_filename[:-4] + '.stemmed.txt') as file:
        stop_words = file.read().splitlines()
else:
    print('  Stop words are not stemmed. It can take a while.')
    with open(stop_words_filename) as file:
        lines = file.read().splitlines()
        for index, stop_word in enumerate(lines):
            stemmed_stop_word = stemmer.stem(stop_word)
            if stemmed_stop_word != '':
                stop_words.append(
                    unicodedata.normalize('NFKD', stemmed_stop_word).encode('ASCII', 'ignore').decode('ASCII'))
            if (index + 1) % 20 == 0:
                print('    ' + "{0:.2f}".format((index * 100) / len(lines)) + '%')
    with open(stop_words_filename[:-4] + '.stemmed.txt', mode='w') as file:
        file.write('\n'.join(stop_words))
    print('  Stemming done. Results cached.')

corpus = {}
print('Loading corpus')
with open('corpus.txt') as file:
    for line in file.read().splitlines():
        if line != '':
            parts = line.split(':', 1)
            corpus[parts[0].strip()] = parts[1].strip()

for label, filename in corpus.items():
    if os.path.isfile(filename[:-4] + '.stemmed.txt'):
        print("  Using cached stemmed version of " + filename)
    else:
        print("  File " + filename + " is not stemmed. It can take a while.")

        with open(filename) as file:
            processed_lines = []
            lines = file.read().split('\n')
            for index, line in enumerate(lines):
                words = []
                for word in re.compile(r'[\w\-]+').findall(line):
                    words.append(stemmer.stem(word))
                processed_lines.append(' '.join(words))
                if (index + 1) % 5 == 0:
                    print('    ' + "{0:.2f}".format((index * 100) / len(lines)) + '%')

        with open(filename[:-4] + '.stemmed.txt', mode='w') as file:
            file.write('\n'.join(processed_lines))
        print('  Stemming done. Results cached.')

    corpus[label] = filename[:-4] + '.stemmed.txt'

params = {
    'min_df': 2,
    'strip_accents': 'ascii',
    'analyzer': 'word',
    'token_pattern': r'[\w\-]+',
    'ngram_range': (1, 2),
    'stop_words': stop_words,
    'norm': 'l2',
    'max_df': 0.5
}


vectorizer = TfidfVectorizer(**params)
features = []

print("Extracting words")
try:
    for label, filename in corpus.items():
        print("  from " + filename)
        with open(filename) as file:
            features += vectorizer.fit(file.read().split('\n')).get_feature_names()

except ValueError as error:
    print("Error: " + str(error))
    sys.exit()

features = sorted(set(features))

params['vocabulary'] = features

vectorizer = TfidfVectorizer(**params)

target = []
lines = []
print('Computing tf-idf')
for label, filename in corpus.items():
    with open(filename) as file:
        parts = file.read().split('\n')
        lines.extend(parts)
        target += [label] * len(parts)

out = vectorizer.fit_transform(lines)

print('Teaching model')
clf = linear_model.SGDClassifier()
clf.fit(out, target)


print('Ready for testing')

for line in sys.stdin:
    line = preprocessor(line.strip())

    with io.StringIO() as f:
        f.write(line)
        f.seek(0)
        result = vectorizer.transform(f)

    print(clf.predict(result)[0])

