import sys
import nltk
import codecs
import re
import os
from nltk import word_tokenize

#nltk.download('punkt')

from nltk.corpus import PlaintextCorpusReader


def validate_informative_aspect(text):
    if "<who>" in text:
        if "</who>" not in text:
            raise AssertionError("who has error")
    else:
        raise AssertionError("who is not present in the document")


def process_corpus():
    corpus_root = "./../CleanNews/"
    for filename in os.listdir(corpus_root):
        try:
            custom_file = open(corpus_root + filename, 'r', encoding='utf8')
            custom_text = custom_file.read()
            validate_informative_aspect(custom_text)
        except AssertionError as er:
            print(filename)
            print(er)

print(sys.version_info)
print(sys.version)
if __name__ == "__main__":
    process_corpus()

'''
#custom_annotation = re.findall(r'<who>(.+?)<\/who>', custom_text)


# nltk.download()


corpus = PlaintextCorpusReader(corpus_root, '.*')

document = corpus.fileids()[0]

raw_document = nltk.data.find('D:/github/Palantir/CleanNews/aeropuerto-jorge-chavez-mexicanos-habrian-querido-sacar-droga-noticia-1904116.txt')

f = codecs.open(raw_document)
for line in f:
    line = line.strip()

wordlist = [w for w in corpus.words(document) if w.islower()]


for w in wordlist:
    print(w)




#custom_nltk_text = nltk.Text(custom_text)


#custom_annotation = re.findall(r'<who>[\s\S]*?<\/who>', custom_text)

#custom_annotation = re.findall(r'<who>(.+?)<\/who>', custom_text)



print(custom_annotation)

#custom_tokenize = word_tokenize(custom_text, 'spanish')




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
'''



'''print(word_list.fileids())
'''

'''
if __name__ == '__main__':
    read_all_annotate()
'''