import glob
import os

import unicodedata
from string import punctuation

from nltk import word_tokenize, SnowballStemmer
from nltk.corpus import stopwords, PlaintextCorpusReader


class StemmingController:
    def __init__(self):
        ADDITIONAL_STOPWORDS = ['%', '?', '¿', 'please', 'your', 'flash', 'plugin', 'Tags', 'MÁS', 'EN', '.+MÁS',
                                '+Tags', '...', ',', '.', '[', ']', '"', '(',
                                ')', '…', 'el', 'la', 'los', 'uno', 'una', '-', ':', '``', "''"]
        self.ALL_STOPWORDS = set(stopwords.words('spanish') + ADDITIONAL_STOPWORDS)
        self.DELIMITER = '\\'


    def stemming_text(self, words):

        stemmer = SnowballStemmer("spanish")
        final_text = []
        for word in words:
            final_text.append(stemmer.stem(word))
        return final_text

    def stemming_files(self, source_folder, destination_folder):
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        corpus_news = PlaintextCorpusReader(source_folder, '.*\.txt')

        for file in corpus_news.fileids():
            file_name = os.path.basename(os.path.normpath(file))
            words = corpus_news.words(file)
            stemmed_content = self.stemming_text(words )
            with open(destination_folder + "/" + file_name, 'w', encoding='utf8') as modified:
                modified.write(' '.join(stemmed_content))