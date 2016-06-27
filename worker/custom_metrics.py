import nltk
import pickle

from nltk.corpus import PlaintextCorpusReader

from worker.document_helper import *
from nltk.metrics.scores import *

class custom_metrics:
    def __init__(self):
        self.DELIMITER = '\\'

    def calculate_metrics(self, classifier, word_features, test_features):

        Gold = []
        Test = []

        TP = 0
        TN = 0
        FP = 0
        FN = 0

        for (features, category) in test_features:
            Gold.append(category)
            result = classifier.classify(features)
            if category == result == 'attack':
                TP += 1
            elif category == result == 'nonattack':
                TN += 1
            elif category != 'attack' and result == 'attack':
                FP += 1
            elif category == 'nonattack' and result == 'attack':
                FN += 1
            Test.append(result)

        Accuracy = (TP + TN) / len(test_features)
        Precision = TP / (TP + FP)
        Recall = TP / (TP + FN)
        F1 = (2 * Precision * Recall) / (Precision + Recall)

        return Accuracy, Precision, Recall, F1, Gold, Test

    def calculate_errors(self, classifier, word_features, test_path, log=0):
        # load the pickle file with the classifier progress

        corpus_news = PlaintextCorpusReader(test_path, '.*\.txt')

        Gold = []
        Test = []

        TP = 0
        TN = 0
        FP = 0
        FN = 0

        Errors = []

        for file in corpus_news.fileids():
            category = file.split(self.DELIMITER)[-1].split('--')[0]
            Gold.append(category)
            words = corpus_news.words(file)
            testing_set = get_features(set(words), word_features)
            result = classifier.classify(testing_set)
            Test.append(result)
            if category == result == 'attack':
                TP += 1
            elif category == result == 'nonattack':
                TN += 1
            elif category != 'attack' and result == 'attack':
                Errors.append('{} : false positive {}'.format(file, result))
                FP += 1
            elif category == 'nonattack' and result == 'attack':
                Errors.append('{} : false negative {}'.format(file, result))
                FN += 1

        Accuracy = (TP + TN) / len(corpus_news.fileids())
        Precision = TP / (TP + FP)
        Recall = TP / (TP + FN)
        F1 = (2 * Precision * Recall) / (Precision + Recall)

        if log == 1:
            self.PrintResult(Accuracy, Precision, Recall, F1, Gold, Test)

        return Errors

    def corpus_metrics(self, corpus_path):
        corpus_news = PlaintextCorpusReader(corpus_path, '.*\.txt')

        print('Corpus documents',  len(corpus_news.fileids()))
        print('Train documents', len([c for c in corpus_news.fileids() if c.startswith('train')]))
        print('Dev documents', len([c for c in corpus_news.fileids() if c.startswith('dev')]))
        print('Test documents', len([c for c in corpus_news.fileids() if c.startswith('test')]))

        words = set(corpus_news.words())
        words = sorted(words)
        print('Corpus different words', len(words))






    def PrintResult(self, Accuracy, Precision, Recall, F1, Gold, Test):
        print('====================================================================================')
        print('Accuracy:', Accuracy)
        print('Precision:', Precision)
        print('   Recall:', Recall)
        print('F-Measure:', F1)
        cm = nltk.ConfusionMatrix(Gold, Test)
        print(cm.pretty_format(sort_by_count=True, show_percents=True, truncate=9))
        print('====================================================================================')