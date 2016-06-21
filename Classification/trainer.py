"""
This script process all the clean news, to determine if they are into 'policiales' or 'nonattack' category
"""
import os
import glob
import random
import pickle
import unicodedata
from nltk import NaiveBayesClassifier, FreqDist, classify
from nltk.corpus import stopwords, PlaintextCorpusReader
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.pipeline import Pipeline
from string import punctuation

ADDITIONAL_STOPWORDS = ['Tags', 'MÁS', 'EN', '.+MÁS', '+Tags', '...', ',', '.', '[', ']', '"', '(',
                        ')', '…', 'el', 'la', 'los', 'uno', 'una', '-', ':', '``', "''"]

ALL_STOPWORDS = set(stopwords.words('spanish') + ADDITIONAL_STOPWORDS)


def get_documents_words(news_files, corpus_news):
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
        category = file.split('/')[-1].split('--')[0]
        file_name = file.replace(root, '', 1)
        words = corpus_news.words(file_name[1:])
        news.append((list(words), category))
    random.shuffle(news)
    return news


def find_features(document, word_features):
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


def vectorize_documents(root_folder, extension='txt'):
    """
    In construction
    :param root_folder:
    :param extension:
    :return:
    """
    # pipeline = Pipeline([
    #     ('vectorizer', CountVectorizer()),
    #     ('tfidfTrans', TfidfVectorizer()),
    #     ('sgdclf', SGDClassifier(loss='modied_huber'))
    # ])
    #
    # params = { 'vectorizer__max_df': (0.5, 1.0),
    #            'vectorizer__ngrams_range': {(1, 1), (1, 2)},
    #            'tfidfTrans__use_idf': (True, False),
    #            'sgdclf__alpha': (0.0001, 0.00001, 0.000001)
    #            }

    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
    news_files = glob.glob(root_folder + "/*." + extension)
    news_content = []
    for file in news_files:
        with open(file, 'r') as news_file:
            content = news_file.read()
        news_content.append(content)

    features_train = news_content[:3]
    features_test = news_content[150:]
    fit = vectorizer.fit(features_train)
    features_train_transformed = vectorizer.fit_transform(features_train)
    features_test_transformed = vectorizer.transform(features_test)
    # print(fit)
    for w in features_train:
        print(w)
    # print(features_train)
    print('TRAINED FEATURES: \n', features_train_transformed[0])
    # print('TESTED FEATURES: \n', features_test_transformed[0])


def train_classifier(root_folder, train_folder, devtest_folder, files_extension='txt'):
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
    words_train_docs = get_documents_words(train_news_files, corpus_news)
    words_devtest_docs = get_documents_words(devtest_news_files, corpus_news)

    all_words = FreqDist(word.lower() for word in corpus_news.words())
    word_features = list(all_words.keys())

    with open('word_features.pickle', 'wb') as words_saver:
        pickle.dump(word_features, words_saver)

    training_set = [(find_features(news, word_features), category) for (news, category) in words_train_docs]
    with open('training_set.pickle', 'wb') as training_writer:
        pickle.dump(training_set, training_writer)
    testing_set = [(find_features(news, word_features), category) for (news, category) in words_devtest_docs]
    with open('devtesting_set.pickle', 'wb') as devtesting_writer:
        pickle.dump(testing_set, devtesting_writer)

    classifier = NaiveBayesClassifier.train(training_set)

    accuracy = classify.accuracy(classifier, testing_set)

    print('Naive Bayes accuracy percent: ', (accuracy * 100))
    classifier.show_most_informative_features(20)
    # saves classifier progress to a pickle file
    with open('naives_classifier.pickle', 'wb') as save_classifier:
        pickle.dump(classifier, save_classifier)


def compare_classifiers_accuracy():
    with open('naives_classifier.pickle', 'rb') as read_classifier:
        naive_bayes_classifier = pickle.load(read_classifier)
    with open('training_set.pickle', 'rb') as training_reader:
        training_set = pickle.load(training_reader)
    with open('devtesting_set.pickle', 'rb') as devtesting_reader:
        devtesting_set = pickle.load(devtesting_reader)

    accuracy = classify.accuracy(naive_bayes_classifier, devtesting_set)
    print('Naive Bayes accuracy percent: ', (accuracy * 100))

    mnb_classifier = SklearnClassifier(MultinomialNB())
    mnb_classifier.train(training_set)
    mnb_accuracy = classify.accuracy(mnb_classifier, devtesting_set)
    print('MNB accuracy percent: ', (mnb_accuracy * 100))

    bernoullinb_classifier = SklearnClassifier(BernoulliNB())
    bernoullinb_classifier.train(training_set)
    bernoullinb_accuracy = classify.accuracy(bernoullinb_classifier, devtesting_set)
    print('BernoulliNB accuracy percent: ', (bernoullinb_accuracy * 100))

    # gaussiannb_classifier = SklearnClassifier(GaussianNB())
    # gaussiannb_classifier.train(training_set)
    # gaussiannb_accuracy = classify.accuracy(gaussiannb_classifier, devtesting_set)
    # print('GaussianNB accuracy percent: ', (gaussiannb_accuracy * 100))

    logisticregression_classifier = SklearnClassifier(LogisticRegression())
    logisticregression_classifier.train(training_set)
    logisticregression_accuracy = classify.accuracy(logisticregression_classifier, devtesting_set)
    print('LogisticRegression accuracy percent: ', (logisticregression_accuracy * 100))

    sgdclassifier_classifier = SklearnClassifier(SGDClassifier())
    sgdclassifier_classifier.train(training_set)
    sgdclassifier_accuracy = classify.accuracy(sgdclassifier_classifier, devtesting_set)
    print('SGDClassifier accuracy percent: ', (sgdclassifier_accuracy * 100))

    svc_classifier = SklearnClassifier(SVC())
    svc_classifier.train(training_set)
    svc_accuracy = classify.accuracy(svc_classifier, devtesting_set)
    print('SVC accuracy percent: ', (svc_accuracy * 100))

    linearsvc_classifier = SklearnClassifier(LinearSVC())
    linearsvc_classifier.train(training_set)
    linearsvc_accuracy = classify.accuracy(linearsvc_classifier, devtesting_set)
    print('LinearSVC accuracy percent: ', (linearsvc_accuracy * 100))

    nusvc_classifier = SklearnClassifier(NuSVC())
    nusvc_classifier.train(training_set)
    nusvc_accuracy = classify.accuracy(nusvc_classifier, devtesting_set)
    print('NuSVC accuracy percent: ', (nusvc_accuracy * 100))


def classify_document(file_name):
    """
    Load words and naives classifier from pickle and recognize a file
    :param file_name: File name for clean text
    :return: Category obtained from text sent
    """
    # load the pickle file with the classifier progress
    with open('naives_classifier.pickle', 'rb') as read_classifier:
        naive_bayes_classifier = pickle.load(read_classifier)
    with open('word_features.pickle', 'rb') as words_reader:
        word_features = pickle.load(words_reader)
    with open(file_name, 'r') as file_text:
        text = file_text.read()
    text_feature = find_features(text, word_features)
    result = naive_bayes_classifier.classify(text_feature)
    return result


def clean_tokenize(doc):
    """
    Clean document, removing accents, punctuation and symbols
    :param doc: string to clean
    :return: string cleaned without punctuation and stop words
    """
    doc = doc.replace('\n', ' ').replace('\r', '').replace('”', '').replace('“', '')
    nfkd_form = unicodedata.normalize('NFKD', doc)
    unicode_doc = u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()
    clean_doc = unicode_doc.translate(punctuation)
    words = word_tokenize(clean_doc)
    clean = []
    for word in words:
        if word not in ALL_STOPWORDS:
            clean.append(word)
    return clean


def tokenize_files(source_folder, destination_folder):
    """
    Search for all the txt files in source folder and clean them
    :param source_folder: Source folder with news to clean
    :param destination_folder: Destination folder where news will be created
    :return: void - Generates all the destination files with clean text
    """
    news = glob.glob(source_folder + "/*.txt")
    for news_file in news:
        file_name = news_file.split('/')[1]
        with open(news_file, 'r') as original:
            doc_text = original.read()
        tokenize_cont = clean_tokenize(doc_text)
        with open(destination_folder+"/"+file_name, 'w') as modified:
            modified.write(' '.join(tokenize_cont))


def docs_tfidf(file, max_features=5000, ngram_range=(1, 1), max_df=.8):
    """

    :param file:
    :param max_features:
    :param ngram_range:
    :param max_df:
    :return:
    """
    vec = TfidfVectorizer(input=file,
                          max_features=max_features,
                          ngram_range=ngram_range,
                          max_df=max_df)
    return vec
    # X = vec.fit_transform(clean_articles)
    # return X, vec


def rename_files(source_folder, extension='txt'):
    """

    :param source_folder:
    :param extension:
    :return:
    """
    news = glob.glob(source_folder + "/*." + extension)
    for news_file in news:
        if news_file.startswith(source_folder + "/policiales--"):
            updated_name = source_folder + '/attack--' + news_file.split('/')[-1].split('--')[-1]
            os.rename(news_file, updated_name)
        elif not news_file.startswith(source_folder + "/attack--"):
            updated_name = source_folder + '/nonattack--' + news_file.split('/')[-1].split('--')[-1]
            os.rename(news_file, updated_name)


def remove_first_line(source_folder, extension):
    """

    :param source_folder:
    :param extension:
    :return:
    """
    files = glob.glob(source_folder + '/*.' + extension)
    for file in files:
        with open(file, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(file, 'w') as fout:
            fout.writelines(data[1:])


# remove_first_line('cleanNews', 'txt')

# tokenize_files('cleanNews', 'corporaNews')

# train_classifier('corpusnews', 'train', 'devtest')

compare_classifiers_accuracy()

# classify_document('corporaNews/nonattack--india-espera-compartir-experiencias-gobierno-ppk-noticia-1910298.txt')

# vectorize_documents('corporaNews','txt')
