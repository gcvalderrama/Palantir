import glob
import os

import unicodedata
from string import punctuation

from nltk import word_tokenize
from nltk.corpus import stopwords


class TokenizerController:
    def __init__(self):
        ADDITIONAL_STOPWORDS = ['.', '%', '-', "'", '?', '¿', 'please', 'your', 'flash', 'plugin', 'Tags', 'MÁS', 'EN',
                                '.+MÁS', "’", "‘"
                                '+Tags', '...', ',', '.', '[', ']', '"', '(',
                                ')', '…', 'el', 'la', 'los', 'uno', 'una', '-', ':', '``', "''"]
        self.ALL_STOPWORDS = set(stopwords.words('spanish') + ADDITIONAL_STOPWORDS)
        self.DELIMITER = '\\'
        # self.DELIMITER = '/'mac

    def tokenize_files(self, source_folder, destination_folder):
        """
        Search for all the txt files in source folder and clean them
        :param source_folder: Source folder with news to clean
        :param destination_folder: Destination folder where news will be created
        :return: void - Generates all the destination files with clean text
        """
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        news = glob.glob(source_folder + "/*.txt")
        for news_file in news:
            file_name = news_file.split(self.DELIMITER)[-1]
            with open(news_file, 'r', encoding='utf8') as original:
                doc_text = original.read()
            tokenize_content = self.clean_tokenize(doc_text)
            with open(destination_folder + "/" + file_name, 'w', encoding='utf8') as modified:
                modified.write(' '.join(tokenize_content))

    def clean_tokenize(self, input_text):
        """
        Clean document, removing accents, punctuation and symbols
        :param text: string to clean
        :return: string cleaned without punctuation and stop words
        """
        text = input_text.replace('\n', ' ').replace('\r', '').replace('”', '').replace('“', '')
        nfkd_form = unicodedata.normalize('NFKD', text)
        unicode_text = u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()
        clean_text = unicode_text.translate(punctuation)
        words = word_tokenize(clean_text)
        final_text = []
        for word in words:
            if word not in self.ALL_STOPWORDS:
                final_text.append(word)
        return final_text