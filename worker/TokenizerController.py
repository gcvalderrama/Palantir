import glob
import os

import unicodedata
from string import punctuation

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords


class TokenizerController:
    def __init__(self):
        ADDITIONAL_STOPWORDS = ['.', '%', '-', "'", '?', '¿', 'please', 'your', 'flash', 'plugin', 'tags', 'mas', 'en',
                                '.+mas', "’", "‘"
                                '+tags', '...', ',', '.', '[', ']', '"', '(',
                                ')', '…', 'el', 'la', 'los', 'uno', 'una', '-', ':', '``', "''"]

        #self.ALL_STOPWORDS = set(stopwords.words('spanish') + ADDITIONAL_STOPWORDS)
        self.ALL_STOPWORDS = set(ADDITIONAL_STOPWORDS)
        self.DELIMITER = '\\'
        self.sent_tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
        # self.DELIMITER = '/'  # mac

    def tokenize_files(self, source_folder, destination_folder,
                       encoding = "uft8", uppercase = False ,
                       accentmark = False, minimunlen = 0, numeric = False, alpha= True,
                       stopwords = True):
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
            with open(news_file, 'r', encoding=encoding) as original:
                doc_text = original.read()

            if not uppercase:
                doc_text = doc_text.lower()

            with open(destination_folder + "/" + file_name, 'w', encoding=encoding) as modified:
                sents = self.sent_tokenizer.tokenize(doc_text)
                for s in sents:
                    tokenize_content = self.clean_tokenize(s, accentmark, minimunlen, numeric, alpha,stopwords)
                    modified.write(' '.join(tokenize_content))
                    modified.write(os.linesep)


    def clean_tokenize(self, input_text, accentmark, minimunlen, numeric, alpha,stopwords):
        """
        Clean document, removing accents, punctuation and symbols
        :param text: string to clean
        :return: string cleaned without punctuation and stop words
        """
        final_text = []
        if not accentmark:
            text = input_text.replace('\n', ' ').replace('\r', '').replace('”', '').replace('“', '').replace('.', '')
            nfkd_form = unicodedata.normalize('NFKD', text)
            unicode_text = u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()
            clean_text = unicode_text.translate(punctuation)
            clean_text = str(''.join([i if ord(i) < 128 else ' ' for i in clean_text])).lower()
            words = word_tokenize(clean_text, language='spanish')
            #words = nltk.regexp_tokenize(clean_text, r"([a-zA-Z])*")
        else:
            text = u"".join([c for c in input_text if not unicodedata.combining(c)])
            words = word_tokenize(text, language='spanish')
        for word in words:
            result = True
            if len(word) > minimunlen:
                if stopwords:
                    if word.lower() in self.ALL_STOPWORDS:
                        result = False

                if result and numeric and word.isnumeric():
                    result = False
                elif result and alpha and not word.isalpha():
                    result = False
                if result:
                    final_text.append(word)

        return final_text