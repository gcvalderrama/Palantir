
import nltk
from nltk import NaiveBayesClassifier, FreqDist, classify
from nltk.corpus import stopwords, PlaintextCorpusReader  # , movie_reviews
from nltk.tokenize import word_tokenize  # , WordPunctTokenizer
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.pipeline import Pipeline
from string import punctuation
import os
import glob
import random
import pickle
import unicodedata

ADDITIONAL_STOPWORDS = ['Tags', 'MÁS', 'EN', 'Tags relacionados', '.+MÁS', '+Tags', '...', ',', '.', '[', ']', '"', '(',
                        ')', '…', 'el', 'la', 'los', 'uno', 'una', '-', ':', '``', "''"]
ALL_STOPWORDS = set(stopwords.words('spanish') + ADDITIONAL_STOPWORDS)
# print(punctuation)


def get_documents_words(news_files, corpus_news):
    news = []
    for file in news_files:
        file_name = file.split('/')[-1]
        category = file_name.split('--')[0]
        words = corpus_news.words(file_name)
        news.append((list(words), category))
    random.shuffle(news)
    return news


def find_features(document, word_features):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features


# def word_feats(words):
#     return dict([(word, True) for word in words])
# negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
# posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]


def vectorize_documents(root_folder, extension='txt'):
    #
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


def classify_documents(root_folder, files_extension='txt'):
    # tokenize_files('CleanNews', 'corporaNews')  # Clean and extract information
    news_files = glob.glob(root_folder + "/*." + files_extension)
    corpus_news = PlaintextCorpusReader(root_folder, '.*\.' + files_extension)
    words_per_doc = get_documents_words(news_files, corpus_news)
    all_words = []
    for w in corpus_news.words():
        all_words.append(w.lower())
    all_words = FreqDist(all_words)
    word_features = list(all_words.keys())

    # with open('word_features.pickle', 'wb') as words_saver:
    #     pickle.dump(word_features, words_saver)

    feature_sets = [(find_features(news, word_features), category) for (news, category) in words_per_doc]
    training_set = feature_sets[:200]
    testing_set = feature_sets[200:]
    classifier = NaiveBayesClassifier.train(training_set)
    # accuracy = classify.accuracy(classifier, testing_set)

    test_ft = [fs for (fs, l) in testing_set]
    result = classifier.classify(test_ft[2])
    print('Test sent: ', test_ft[2])
    print('Result: ', result)
    # print('Naive Bayes accuracy percent: ', (accuracy * 100))
    # classifier.show_most_informative_features(20)
    # # saves classifier progress to a pickle file
    # with open('naives_classifier.pickle', 'wb') as save_classifier:
    #     pickle.dump(classifier, save_classifier)


def classify_document(file_name):
    # load the pickle file with the classifier progress
    with open('naives_classifier.pickle', 'rb') as read_classifier:
        naive_bayes_classifier = pickle.load(read_classifier)
    with open('word_features.pickle', 'rb') as words_reader:
        word_features = pickle.load(words_reader)
    with open(file_name, 'r') as file_text:
        text = file_text.read()
    text_feature = find_features(text, word_features)
    result = naive_bayes_classifier.classify(text_feature)
    print('Test sent: ', text_feature)
    print('Result: ', result)


def clean_tokenize(doc):
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
    print(ALL_STOPWORDS)
    # with open(destination_folder + "/All_Stopwords.txt", 'w') as stopwords:
    #     stopwords.write('\n'.join(ALL_STOPWORDS))
    news = glob.glob(source_folder + "/*.txt")
    for news_file in news:
        fname = news_file.split('/')[1]
        with open(news_file, 'r') as original:
            doc_text = original.read()
        tokenize_cont = clean_tokenize(doc_text)
        with open(destination_folder+"/"+fname, 'w') as modified:
            modified.write(' '.join(tokenize_cont))


def docs_tfidf(file, max_features=5000, ngram_range=(1, 1), max_df=.8):
    vec = TfidfVectorizer(input=file,
                          max_features=max_features,
                          ngram_range=ngram_range,
                          max_df=max_df)
    return vec
    # X = vec.fit_transform(clean_articles)
    # return X, vec


def write_file_summary(source_folder, file_name):
    news = glob.glob(source_folder + "/*.txt")
    with open(file_name, 'w') as summ:
        summ.write("\n".join(news))


def rename_files(source_folder, extension='txt'):
    news = glob.glob(source_folder + "/*." + extension)
    for news_file in news:
        if not news_file.startswith(source_folder + "/policiales--"):
            updated_name = source_folder + '/nopoliciales--' + news_file.split('/')[-1].split('--')[-1]
            os.rename(news_file, updated_name)


def remove_first_line(source_folder, extension):
    files = glob.glob(source_folder + '/*.' + extension)
    for file in files:
        with open(file, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(file, 'w') as fout:
            fout.writelines(data[1:])


# remove_first_line('CleanNews', 'txt')

# tokenize_files('CleanNews', 'corporaNews')
# classify_documents('corporaNews')
# rename_files('CleanNews')
classify_document('corporaNews/nopoliciales--india-espera-compartir-experiencias-gobierno-ppk-noticia-1910298.txt')
# vectorize_documents('corporaNews','txt')




