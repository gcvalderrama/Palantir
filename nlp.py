from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import json
import scipy
import glob
import nltk
from selenium import webdriver

# nltk.download()

ADDITIONAL_STOPWORDS = [',', 'editor']
ALL_STOPWORDS = set(stopwords.words('spanish') + ADDITIONAL_STOPWORDS)


def clean_tokenize(doc):
    doc = str(''.join([i if ord(i) < 128 else ' ' for i in doc])).lower()
    doc = doc.translate(punctuation)
    t = word_tokenize(doc)
    clean = []
    for word in t:
        if word not in ALL_STOPWORDS:
            clean.append(word)
    return clean


def tokenize_files(source_folder, destination_folder):
    print(ALL_STOPWORDS)
    with open(destination_folder + "/All_Stopwords.txt", 'w') as stopwords:
        stopwords.write('\n'.join(ALL_STOPWORDS))
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

xxxx = docs_tfidf('summary.txt')
print(xxxx)
# write_file_summary('Tokenized', 'summary.txt')
# tokenize_files('CleanTokenize', 'Tokenized')
