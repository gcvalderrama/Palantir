
import glob
import nltk
import shutil
import os
from worker import Crawler, Helper, Trainer


# # extract news from url and save them
# webCrawler = Crawler()
# webCrawler.extract_web_news('news', 'http://elcomercio.pe/feed/lima/policiales.xml', 'attack')
# webCrawler.extract_web_news('news', 'http://elcomercio.pe/feed/politica/actualidad.xml', 'nonattack')
# webCrawler.extract_web_news('news', 'http://elcomercio.pe/feed/tecnologia.xml', 'nonattack')
# webCrawler.extract_web_news('news', 'http://elcomercio.pe/feed/gastronomia.xml', 'nonattack')
#
# # clean html tags
# webCrawler.clean_raw_news('news', '00', True)
#
# # removing first line with date - avoiding noise
from worker.StemmingController import StemmingController
from worker.TokenizerController import TokenizerController
from worker.cross_validation import build_folds
from worker.custom_metrics import custom_metrics



helper = Helper()
# helper.remove_first_line('00', 'txt')
#
# # remove '?ref_bajada' from files name
# helper.clean_file_name('news/clean')
# helper.clean_file_name('news/raw', 'html')

# remove stop words from news and prepare text for training


if os.path.exists('./01/selected_news'):
    shutil.rmtree('./01/selected_news')
if os.path.exists('./01/clean_news'):
    shutil.rmtree('./01/clean_news')
if os.path.exists('./01/'):
    shutil.rmtree('./01/')

news_trainer = Trainer()
metrics = custom_metrics()
tokenizerctr = TokenizerController()

stemmingController = StemmingController()

tokenizerctr.tokenize_files('00/anotador_01', '01/tokenized')
#stemmingController.stemming_files('01/tokenized', '01/stemming')

build_folds('01/tokenized', '01/cross')

metrics.corpus_metrics('01/cross/0')






Total_Naive_Accurancy = 0
Total_MultinomialNB_Accurancy = 0
Total_bernoullinb_Accurancy = 0
Total_LogisticRegression_Accurancy = 0
Total_SGD_Accurancy = 0
Total_SVC_Accurancy = 0
Total_LINEARSVC_Accurancy = 0
Total_NUSVC_Accurancy = 0
for i in range(0):
    word_features, training_set, dev_set, test_set = news_trainer.build_train_dev_test_set('01/cross/' + str(i),
                                                                                           'train', 'dev', 'test')
    '#naive bayes'
    classifier = news_trainer.naives_classifier(training_set, dev_set, 0)
    Accuracy, Precision, Recall, F1, Gold, Test = metrics.calculate_metrics(classifier, word_features, test_set)
    Total_Naive_Accurancy += Accuracy

    classifier = news_trainer.MultinomialNB_classifier(training_set, dev_set)
    Accuracy, Precision, Recall, F1, Gold, Test = metrics.calculate_metrics(classifier, word_features, test_set)
    Total_MultinomialNB_Accurancy += Accuracy

    classifier = news_trainer.bernoullinb_classifier(training_set, dev_set)
    Accuracy, Precision, Recall, F1, Gold, Test = metrics.calculate_metrics(classifier, word_features, test_set)
    Total_bernoullinb_Accurancy += Accuracy

    classifier = news_trainer.logisticregression_classifier(training_set, dev_set)
    Accuracy, Precision, Recall, F1, Gold, Test = metrics.calculate_metrics(classifier, word_features, test_set)
    Total_LogisticRegression_Accurancy += Accuracy

    classifier = news_trainer.sgdclassifier_classifier(training_set, dev_set)
    Accuracy, Precision, Recall, F1, Gold, Test = metrics.calculate_metrics(classifier, word_features, test_set)
    Total_SGD_Accurancy += Accuracy

    classifier = news_trainer.svc_classifier(training_set, dev_set)
    Accuracy, Precision, Recall, F1, Gold, Test = metrics.calculate_metrics(classifier, word_features, test_set)
    Total_SVC_Accurancy += Accuracy

    classifier = news_trainer.linearsvc_classifier(training_set, dev_set)
    Accuracy, Precision, Recall, F1, Gold, Test = metrics.calculate_metrics(classifier, word_features, test_set)
    Total_LINEARSVC_Accurancy += Accuracy

    classifier = news_trainer.nusvc_classifier(training_set, dev_set)
    Accuracy, Precision, Recall, F1, Gold, Test = metrics.calculate_metrics(classifier, word_features, test_set)
    Total_NUSVC_Accurancy += Accuracy

    #news_trainer.save_train_dev_set(word_features, training_set, dev_set, test_set)
    #errors = metrics.calculate_errors(classifier, word_features, '01/cross/' + str(i) + '/test/')

    #for f in errors:
    #    print(f)
    #metrics.PrintResult(Accuracy, Precision, Recall, F1, Gold, Test)


print('Total NAIVE BAYES Accurancy {}'.format(Total_Naive_Accurancy/10))
print('Total Multinomial NAIVE BAYES Accurancy {}'.format(Total_MultinomialNB_Accurancy /10))
print('Total Logistic Regression Accurancy {}'.format(Total_LogisticRegression_Accurancy /10))
print('Total SGD NAIVE BAYES Accurancy {}'.format(Total_SGD_Accurancy /10))
print('Total SVC Accurancy {}'.format(Total_SVC_Accurancy /10))
print('Total LENEAR SVC Accurancy {}'.format(Total_LINEARSVC_Accurancy /10))
print('Total NU SVC Accurancy {}'.format(Total_NUSVC_Accurancy /10))