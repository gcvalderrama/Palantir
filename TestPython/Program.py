import sys
import nltk
import codecs
import re

from nltk.corpus import PlaintextCorpusReader

# nltk.download()
print(sys.version_info)
print(sys.version)

corpus_root = "./../CleanNews/"
corpus = PlaintextCorpusReader(corpus_root, '.*')

document = corpus.fileids()[0]

raw_document = nltk.data.find('D:/github/Palantir/CleanNews/aeropuerto-jorge-chavez-mexicanos-habrian-querido-sacar-droga-noticia-1904116.txt')

f = codecs.open(raw_document)
for line in f:
    line = line.strip()




wordlist = [w for w in corpus.words(document) if w.islower()]

for w in wordlist:
    print(w)


try:
    words = corpus.words(document)
    raw_text = corpus.raw(document)
    text = nltk.Text(words)
    concordance = text.concordance("droga")
    sentences = corpus.sents(document)
    num_chars = len(raw_text)
    num_words = len(words)

except AssertionError:
    print('is empty')
    print(document)



'''print(word_list.fileids())
'''

'''
if __name__ == '__main__':
    read_all_annotate()
'''