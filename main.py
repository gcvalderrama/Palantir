
import glob
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
helper = Helper()
# helper.remove_first_line('00', 'txt')
#
# # remove '?ref_bajada' from files name
# helper.clean_file_name('news/clean')
# helper.clean_file_name('news/raw', 'html')

# remove stop words from news and prepare text for training
news_trainer = Trainer()

# destination = {'01/selected_news/train': 80, '01/selected_news/dev': 20, '01/selected_news/test': 20}
# helper.distribute_files('00/anotador_01', destination_folders=destination, split_category='nonattack--')

# cleaning_directories = {'01/selected_news/train': '01/clean_news/corpus/train',
#                         '01/selected_news/dev': '01/clean_news/corpus/dev',
#                         '01/selected_news/test': '01/clean_news/test'}
# for source_folder, destination_folder in cleaning_directories.items():
#     news_trainer.tokenize_files(source_folder, destination_folder)
#
# stemm_directories = {'01/selected_news/train': '01/stemm_news/corpus/train',
#                      '01/selected_news/dev': '01/stemm_news/corpus/dev',
#                      '01/selected_news/test': '01/stemm_news/test'}
# for source_folder, destination_folder in stemm_directories.items():
#     news_trainer.stemming_files(source_folder, destination_folder)

# begin training with normal words
news_trainer.corpus_classifier('01/clean_news/corpus', 'train', 'dev')
news_trainer.compare_classifiers_accuracy()
# test
test_files = glob.glob('01/clean_news/test/*.txt')\
             + glob.glob('01/clean_news/corpus/train/*.txt')\
             + glob.glob('01/clean_news/corpus/dev/*.txt')
for file in test_files:
    category = news_trainer.classify_document(file)
    print('Category : ', category, ' File: ', file)

print('************************************************')
# training with stemmed words
news_trainer.corpus_classifier('01/stemm_news/corpus', 'train', 'dev')
news_trainer.compare_classifiers_accuracy()
# test
test_stemm_files = glob.glob('01/stemm_news/test/*.txt')\
                   + glob.glob('01/stemm_news/corpus/train/*.txt')\
                   + glob.glob('01/stemm_news/corpus/dev/*.txt')
for file in test_stemm_files:
    category = news_trainer.classify_document(file)
    print('Category : ', category, ' File: ', file)

