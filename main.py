
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
# helper = Helper()
# helper.remove_first_line('00', 'txt')
#
# # remove '?ref_bajada' from files name
# helper.clean_file_name('news/clean')
# helper.clean_file_name('news/raw', 'html')

# remove stop words from news and prepare text for training
news_trainer = Trainer()
news_trainer.tokenize_files('00/anotador_01', '01/clean_news')
news_trainer.stemming_files('00/anotador_01', '01/stemm_news')

# begin training with normal words
news_trainer.train_classifier('01', 'clean_news')
news_trainer.compare_classifiers_accuracy()
type = news_trainer.classify_document(
    'classification/corpusnews/devtest/nonattack--india-espera-compartir-experiencias-gobierno-ppk-noticia-1910298.txt')

print('************************************************')
# training with stemmed words
news_trainer.train_classifier('01', 'stemm_news')
news_trainer.compare_classifiers_accuracy()
type = news_trainer.classify_document(
    'classification/corpusnews/devtest/nonattack--india-espera-compartir-experiencias-gobierno-ppk-noticia-1910298.txt')

