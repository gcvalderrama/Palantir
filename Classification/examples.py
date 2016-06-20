
from nltk.corpus import stopwords, PlaintextCorpusReader, movie_reviews, data
from nltk.tokenize import RegexpTokenizer, WordPunctTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from string import punctuation
import glob
import random
import pickle

# nltk.download()

ADDITIONAL_STOPWORDS = ['Tags', 'MÁS', 'EN', 'Tags relacionados', '.+MÁS', '+Tags', '...', ',', '.', '[', ']', '"', '(',
                        ')', '…']
ALL_STOPWORDS = set(stopwords.words('spanish') + ADDITIONAL_STOPWORDS)
print(punctuation)


# Find the directory where the corpus lives.
genesis_dir = data.find('corporaNews')
# Create our custom sentence tokenizer.
my_sent_tokenizer = RegexpTokenizer('[^.!?]+')
# Create the new corpus reader object.
my_genesis = PlaintextCorpusReader('corporaNews', '.*\.txt')
print(my_genesis.words('actualidad--alberto-fujimori-fue-trasladado-emergencia-clinica-local-noticia-1910176.txt'))
# doctest: +NORMALIZE_WHITESPACE


print(movie_reviews.categories())
print('NEGATIVE: ')
print(movie_reviews.fileids('neg'))
print('POSITIVE: ')
print(movie_reviews.fileids('pos'))

documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fields(category)]

documents = []
for category in movie_reviews.categories():
    for fileid in movie_reviews.fileids(category):
        words = movie_reviews.words(fileid)
        documents.append(list(words), category)

random.suffle(documents)


def words(fileid):
    """
    DOES NOT WORK
    Dummy function, to see how the information was extracted
    :param fileid:
    :return:
    """
    encoding = 'utf-8'
    word_tokenizer = WordPunctTokenizer()
    iterator = elt.getiterator()
    out = []

    for node in iterator:
        text = node.text
        if text is not None:
            if isinstance(text, bytes):
                text = text.decode(encoding)
            toks = word_tokenizer.tokenize(text)
            out.extend(toks)
    return out



