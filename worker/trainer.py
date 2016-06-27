"""
This script process all the clean news, to determine if they are into 'attack' or 'nonattack' category
"""
import os
import glob
import math
import random
import pickle
import unicodedata
from nltk import NaiveBayesClassifier, FreqDist, classify
from nltk.corpus import stopwords, PlaintextCorpusReader
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk import ConfusionMatrix
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from string import punctuation


class Trainer:


    def __init__(self):

        ADDITIONAL_STOPWORDS = ['%', '?', '¿',  'please', 'your', 'flash', 'plugin', 'Tags', 'MÁS', 'EN', '.+MÁS', '+Tags', '...', ',', '.', '[', ']', '"', '(',
                            ')', '…', 'el', 'la', 'los', 'uno', 'una', '-', ':', '``', "''"]
        self.ALL_STOPWORDS = set(stopwords.words('spanish') + ADDITIONAL_STOPWORDS)
        self.DELIMITER = '\\'
        #self.DELIMITER = '/'mac

    def get_documents_words(self, news_files, corpus_news):
        """
        Given a set of documents it will return the dictionary with their
        respective categories
        :param news_files: List of raw news file names
        :param corpus_news: PlainTextCorpusReader object
        :return: Dictionary with words and categories associated
        """
        root = corpus_news.root
        news = []
        for file in news_files:
            category = file.split(self.DELIMITER)[-1].split('--')[0]
            file_name = file.replace(root, '', 1)
            words = corpus_news.words(file_name[1:])
            news.append((list(words), category))
        #random.shuffle(news)
        return news

    def find_features(self, document, word_features):
        """
        Given a string with a word_features as universe,
        it will return their respective features
        :param document: String to generate the features to
        :param word_features: Universe of words
        :return: Dictionary with the features for document string
        """
        words = set(document)
        features = {}
        for w in word_features:
            features[w] = (w in words)
        return features

    def save_train_dev_set(self, word_features, training_set, dev_set, test_set):
        with open('word_features.pickle', 'wb') as words_saver:
            pickle.dump(word_features, words_saver)
        with open('training_set.pickle', 'wb') as training_writer:
            pickle.dump(training_set, training_writer)
        with open('devtesting_set.pickle', 'wb') as devtesting_writer:
            pickle.dump(dev_set, devtesting_writer)
        with open('testing_set.pickle', 'wb') as testing_writer:
            pickle.dump(test_set, testing_writer)


    def build_train_dev_test_set(self, root_folder, train_folder, devtest_folder, test_folder):


        train_news_files = glob.glob(root_folder + "/" + train_folder + "/*.txt")
        devtest_news_files = glob.glob(root_folder + "/" + devtest_folder + "/*.txt")
        test_news_files = glob.glob(root_folder + "/" + test_folder + "/*.txt")
        corpus_news = PlaintextCorpusReader(root_folder, '.*\.txt')

        words_train_docs = self.get_documents_words(train_news_files, corpus_news)
        words_devtest_docs = self.get_documents_words(devtest_news_files, corpus_news)
        words_test_docs = self.get_documents_words(test_news_files, corpus_news)

        all_words = FreqDist(word.lower() for word in corpus_news.words())

        word_features = list(all_words.keys())
        training_set = [(self.find_features(news, word_features), category) for (news, category) in words_train_docs]
        dev_set = [(self.find_features(news, word_features), category) for (news, category) in words_devtest_docs]
        test_set = [(self.find_features(news, word_features), category) for (news, category) in words_test_docs]
        return word_features, training_set, dev_set, test_set

    def naives_classifier(self, training_set, dev_set, log=0):

        classifier = NaiveBayesClassifier.train(training_set)
        accuracy = classify.accuracy(classifier, dev_set)

        print('Naive Bayes accuracy dev percent: ', (accuracy * 100))
        if log == 1:
            classifier.show_most_informative_features(20)

        return classifier

    def MultinomialNB_classifier(self, training_set, dev_set):
        mnb_classifier = SklearnClassifier(MultinomialNB())
        mnb_classifier.train(training_set)
        mnb_accuracy = classify.accuracy(mnb_classifier, dev_set)
        print('MNB dev test accuracy percent: ', (mnb_accuracy * 100))
        return mnb_classifier

    def bernoullinb_classifier(self, training_set, dev_set):
        bernoullinb_classifier = SklearnClassifier(BernoulliNB())
        bernoullinb_classifier.train(training_set)
        bernoullinb_accuracy = classify.accuracy(bernoullinb_classifier, dev_set)
        print('BernoulliNB dev accuracy percent: ', (bernoullinb_accuracy * 100))
        return bernoullinb_classifier

    def logisticregression_classifier(self, training_set, dev_set):
        logisticregression_classifier = SklearnClassifier(LogisticRegression())
        logisticregression_classifier.train(training_set)
        logisticregression_accuracy = classify.accuracy(logisticregression_classifier, dev_set)
        print('LogisticRegression dev accuracy percent: ', (logisticregression_accuracy * 100))
        return logisticregression_classifier

    def sgdclassifier_classifier (self, training_set, dev_set):
        sgdclassifier_classifier = SklearnClassifier(SGDClassifier())
        sgdclassifier_classifier.train(training_set)
        sgdclassifier_accuracy = classify.accuracy(sgdclassifier_classifier, dev_set)
        print('SGDClassifier dev accuracy percent: ', (sgdclassifier_accuracy * 100))
        return sgdclassifier_classifier

    def svc_classifier(self, training_set, dev_set):
        svc_classifier = SklearnClassifier(SVC())
        svc_classifier.train(training_set)
        svc_accuracy = classify.accuracy(svc_classifier, dev_set)
        print('SVC dev accuracy percent: ', (svc_accuracy * 100))
        return svc_classifier

    def linearsvc_classifier(self, training_set, dev_set):
        linearsvc_classifier = SklearnClassifier(LinearSVC())
        linearsvc_classifier.train(training_set)
        linearsvc_accuracy = classify.accuracy(linearsvc_classifier, dev_set)
        print('LinearSVC dev accuracy percent: ', (linearsvc_accuracy * 100))
        return linearsvc_classifier

    def nusvc_classifier(self, training_set, dev_set):
        nusvc_classifier = SklearnClassifier(NuSVC())
        nusvc_classifier.train(training_set)
        nusvc_accuracy = classify.accuracy(nusvc_classifier, dev_set)
        print('NuSVC dev accuracy percent: ', (nusvc_accuracy * 100))
        return nusvc_classifier



    def save_classifier(self, classifier, filename):
        with open(filename, 'wb') as save_classifier:
            pickle.dump(classifier, save_classifier)

    def corpus_classifier(self, root_folder, train_folder, devtest_folder, files_extension='txt', log=0):
        """
        Generates .pickle file with trained classifier and words universe
        :param root_folder: Folder that contains train and devtest folders
        :param train_folder: Folder inside root_folder that contains the news to train with
        :param devtest_folder: Folder inside root_folder that contains the new to test with
        :param files_extension: File extension to search for
        :return: void - empty
        """
        train_news_files = glob.glob(root_folder + "/" + train_folder + "/*." + files_extension)
        devtest_news_files = glob.glob(root_folder + "/" + devtest_folder + "/*." + files_extension)
        corpus_news = PlaintextCorpusReader(root_folder, '.*\.' + files_extension)
        words_train_docs = self.get_documents_words(train_news_files, corpus_news)
        words_devtest_docs = self.get_documents_words(devtest_news_files, corpus_news)

        all_words = FreqDist(word.lower() for word in corpus_news.words())
        word_features = list(all_words.keys())

        with open('word_features.pickle', 'wb') as words_saver:
            pickle.dump(word_features, words_saver)
        training_set = [(self.find_features(news, word_features), category) for (news, category) in words_train_docs]
        with open('training_set.pickle', 'wb') as training_writer:
            pickle.dump(training_set, training_writer)
        testing_set = [(self.find_features(news, word_features), category) for (news, category) in words_devtest_docs]
        with open('devtesting_set.pickle', 'wb') as devtesting_writer:
            pickle.dump(testing_set, devtesting_writer)

        classifier = NaiveBayesClassifier.train(training_set)

        accuracy = classify.accuracy(classifier, testing_set)
        print('Naive Bayes accuracy percent: ', (accuracy * 100))
        if log == 1:
            classifier.show_most_informative_features(20)
        # saves classifier progress to a pickle file
        with open('naives_classifier.pickle', 'wb') as save_classifier:
            pickle.dump(classifier, save_classifier)

    def train_classifier(self, root_folder, train_folder, files_extension='txt'):
        """
        Generates .pickle file with trained classifier and words universe
        :param root_folder: Folder that contains train and devtest folders
        :param train_folder: Folder inside root_folder that contains the news to train with
        :param files_extension: File extension to search for
        :return: void - empty
        """
        train_news_files = glob.glob(root_folder + "/" + train_folder + "/*." + files_extension)
        corpus_news = PlaintextCorpusReader(root_folder, '.*\.' + files_extension)
        words_docs = self.get_documents_words(train_news_files, corpus_news)

        all_words = FreqDist(word.lower() for word in corpus_news.words())
        word_features = list(all_words.keys())

        with open('word_features.pickle', 'wb') as words_saver:
            pickle.dump(word_features, words_saver)

        features_set = [(self.find_features(news, word_features), category) for (news, category) in words_docs]
        index = math.floor(len(features_set)/2)
        training_set = features_set[:index]
        testing_set = features_set[index:]

        with open('training_set.pickle', 'wb') as training_writer:
            pickle.dump(training_set, training_writer)
        with open('devtesting_set.pickle', 'wb') as devtesting_writer:
            pickle.dump(testing_set, devtesting_writer)

        classifier = NaiveBayesClassifier.train(training_set)

        accuracy = classify.accuracy(classifier, testing_set)

        print('Naive Bayes accuracy percent: ', (accuracy * 100))
        classifier.show_most_informative_features(20)
        # saves classifier progress to a pickle file
        with open('naives_classifier.pickle', 'wb') as save_classifier:
            pickle.dump(classifier, save_classifier)

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
            with open(destination_folder+"/"+file_name, 'w', encoding='utf8') as modified:
                modified.write(' '.join(tokenize_content))

    def stemming_text(self, input_text):
        """
        Clean document, removing accents, punctuation and symbols and stemm words
        :param text: string to clean
        :return: string cleaned without punctuation and stop words
        """
        text = input_text.replace('\n', ' ').replace('\r', '').replace('”', '').replace('“', '')
        nfkd_form = unicodedata.normalize('NFKD', text)
        unicode_text = u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()
        clean_text = unicode_text.translate(punctuation)
        words = word_tokenize(clean_text)
        stemmer = SnowballStemmer("spanish")
        final_text = []
        for word in words:
            if word not in self.ALL_STOPWORDS:
                final_text.append(stemmer.stem(word))
        return final_text

    def stemming_files(self, source_folder, destination_folder, extension='txt'):
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        file_list = glob.glob(source_folder + "/*." + extension)
        for file in file_list:
            file_name = file.split(self.DELIMITER)[-1]
            with open(file, 'r', encoding='utf8') as original:
                original_text = original.read()
            stemmed_content = self.stemming_text(original_text)
            with open(destination_folder + "/" + file_name, 'w',encoding='utf8') as modified:
                modified.write(' '.join(stemmed_content))


# remove_first_line('cleanNews', 'txt')

# tokenize_files('cleanNews', 'corporaNews')

# train_classifier('corpusnews', 'train', 'devtest')

# compare_classifiers_accuracy()

# classify_document('corporaNews/nonattack--india-espera-compartir-experiencias-gobierno-ppk-noticia-1910298.txt')

# vectorize_documents('corporaNews','txt')
