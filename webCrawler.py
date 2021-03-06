import datetime
import xml.etree.ElementTree as ET
import re
import os
import glob
import os.path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from twitter import *
from bs4 import BeautifulSoup
import unicodedata
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation

ADDITIONAL_STOPWORDS = ['Tags', 'MÁS', 'EN', '.+MÁS', '+Tags', '...', ',', '.', '[', ']', '"', '(',
                        ')', '…', 'el', 'la', 'los', 'uno', 'una', '-', ':', '``', "''"]

ALL_STOPWORDS = set(stopwords.words('spanish') + ADDITIONAL_STOPWORDS)

chromedriver = "/Users/ozo/ExternalDemo/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver


def write_news_file(url):
    browser = webdriver.Firefox()
    browser.get(url)
    data_formatted = browser.page_source.encode('utf-8')
    browser.close()
    file_name = 'news_' + datetime.datetime.now().strftime('%d%m%y%H%M%S') + '.xml'
    f = open('news/' + file_name, 'wb')
    f.write(data_formatted)
    f.flush()
    f.close()


def write_each_news(folder, url, tag):
    browser = webdriver.Firefox()
    browser.get(url)
    list_linker_href = browser.find_elements_by_xpath('//xhtml:a[@href]')
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 10)
    for l in list_linker_href:
        news_url = l.get_attribute('href')
        driver.get(news_url)
        print(news_url)
        wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, 'fecha')))
        fecha = driver.find_element_by_class_name("fecha").get_attribute("datetime")
        file_name = tag + '--' + news_url.split('/')[-1]
        try:
            news_element = driver.find_element_by_id('main-txt-nota')
        except NoSuchElementException:
            print('main-txt-nota not found on ' + file_name)
            continue
        news_content = news_element.get_attribute('innerHTML').encode('utf-8')
        content = fecha + "\n" + news_content.decode('utf-8')
        with open(folder + "/" + file_name + ".html", 'w') as file:
            file.write(content)
    browser.close()
    driver.close()


def write_news(url):
    browser = webdriver.Firefox()
    browser.get(url)
    list_linker_href = browser.find_element_by_css_selector('.entry > h3 > a')
    driver = webdriver.Firefox()
    for l in list_linker_href:
        news_url = l.get_attribute('href')
        driver.get(news_url)
        driver.implicitly_wait(20)
        print(news_url)
        file_name = news_url.split('/')[-1]
        try:
            news_element = driver.find_element_by_id('main-txt-nota')
        except NoSuchElementException:
            print('main-txt-nota not found on ' + file_name)
            break
        news_content = news_element.get_attribute('innerHTML').encode('utf-8')
        f = open('news/' + file_name + '.html', 'wb')
        f.write(news_content)
        f.flush()
        f.close()
    browser.close()
    driver.close()


def search_in_twitter(place_name, place_type, query):
    ACCESS_TOKEN = '228157926-JbzXfMmj8N8dWPTZfJBQc7KGp6VGBecOnfs8hzmo'
    ACCESS_SECRET = 'bGN6fu9ENRuM0b3PYbNobdR7zAvlsimHc6C1J2dbrERWt'
    CONSUMER_KEY = 'MkPdpJrKYW7ObGO73n1RoPQfH'
    CONSUMER_SECRET = 'No06OWAsIkeMnUPx0Tzrqkm6JjcfAUvyO4UD5Sw3kEYJGOydyB'
    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_client = Twitter(auth=oauth)
    result = twitter_client.geo.search(query=place_name, granularity=place_type)
    place_id = result['result']['places'][0]['id']
    print('Surco Twitter id : ' + place_id)
    result = twitter_client.search.tweets(q="place:%s+%s" % (place_id, query))
    print(result['statuses'])
    for tweet in result['statuses']:
        print(tweet['text'] + " | " + tweet['place']['name'] if tweet['place'] else "Undefined place")


def read_and_clean(origin, destination, skip_validation):
    weird_string = '&nbsp;'
    news = glob.glob(origin + "/*.html")
    for news_file in news:
        print(news_file)
        file_name = destination + '/' + news_file.split('/')[1].split('.')[0] + '.txt'
        if skip_validation or not os.path.isfile(file_name):
            with open(news_file, 'r') as rf:
                news_raw = rf.read()
            # news_content = news_raw.split('<style')[0].split('<script')[0].replace(weird_string, " ")
            # clean_content = clean_html(news_content)
            soup = BeautifulSoup(news_raw, 'lxml')  # create a new bs4 object from the html data loaded
            for script in soup(["script", "style"]):  # remove all javascript and stylesheet code
                script.extract()
            # get text
            text = soup.get_text()
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            with open(file_name, 'w') as f:
                f.write(text)


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def remove_tags(text):
    return ''.join(ET.fromstring(text).itertext())


def get_dates():
    news = glob.glob("news/*.html")
    browser = webdriver.Firefox()
    for news_file in news:
        web_url = news_file.split('/')[1].split('.')[0]
        browser.get("http://elcomercio.pe/lima/policiales/"+web_url)
        wait = WebDriverWait(browser, 10)
        wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, 'fecha')))
        fecha = browser.find_element_by_class_name("fecha").get_attribute("datetime")
        with open(news_file, 'r') as original:
            data = original.read()
        with open(news_file, 'w') as modified:
            modified.write(fecha + "\n" + data)
        with open("cleanNews/"+web_url+".txt", 'r') as clean_original:
            data = clean_original.read()
        with open("cleanNews/"+web_url+".txt", 'w') as clean_modified:
            clean_modified.write(fecha + "\n" + data)
    browser.close()


def remove_weird_character():
    weird_String = '&nbsp;'
    news = glob.glob("cleanNews/*.txt")
    for news_file in news:
        with open(news_file, 'r') as original:
            data = original.read()
        data.replace(weird_String, " ")
        with open(news_file, 'w') as modified:
            modified.write(data.replace(weird_String, " "))


def rename_files():
    news = glob.glob("news/*.html")
    for news_file in news:
        if "?ref_bajada" in news_file:
            updated_news_file = news_file.replace('?ref_bajada', '')
            os.rename(news_file, updated_news_file)


def rename_files(source_folder, extension='txt'):
    news = glob.glob(source_folder + "/*." + extension)
    for news_file in news:
        if "?ref_bajada" in news_file:
            updated_news_file = news_file.replace('?ref_bajada', '')
            os.rename(news_file, updated_news_file)
            # news_file = updated_news_file

        # if news_file.startswith(source_folder + "/actualidad--") \
        #         or news_file.startswith(source_folder + "/gastronomia--") \
        #         or news_file.startswith(source_folder + "/tecnologia--"):
        #     updated_name = source_folder + '/nonattack--' + news_file.split('/')[-1].split('--')[-1]
        #     os.rename(news_file, updated_name)
        # else:
        #     updated_name = source_folder + '/attack--' + news_file.split('/')[-1].split('--')[-1]
        #     os.rename(news_file, updated_name)


def read_and_clean(origin, destination, skip_validation):
    """
    Read raw news from origin and after cleaning, it will write them into destination folder
    :param origin: Folder that contains all the raw news
    :param destination: Destination folder to write clear news content
    :param skip_validation: True or False - check file existence
    :return: nothing - void
    """
    news = glob.glob(origin + "/*.html")
    for news_file in news:
        print(news_file)
        file_name = destination + '/' + news_file.split('/')[1].split('.')[0] + '.txt'
        if skip_validation or not os.path.isfile(file_name):
            with open(news_file, 'r') as read_file:
                news_raw = read_file.read()
            # create a new bs4 object from the html data loaded
            soup = BeautifulSoup(news_raw, 'lxml')
            # remove all javascript and stylesheet code
            for script in soup(["script", "style"]):
                script.extract()
            # get text
            text = soup.get_text()
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            with open(file_name, 'w') as write_file:
                write_file.write(text)


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
        file_name = news_file.split('/')[-1]
        with open(news_file, 'r') as original:
            doc_text = original.read()
        tokenize_cont = clean_tokenize(doc_text)
        with open(destination_folder + "/" + file_name, 'w') as modified:
            modified.write(' '.join(tokenize_cont))


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


# rename_files("news", "html")

# remove_weird_character()
# read_and_clean('news', 'corporaNews', True)
# search_in_twitter('Surco', 'neighborhood', 'robo')

# write_each_news('news', 'http://elcomercio.pe/feed/lima/policiales.xml', 'attack')
# write_each_news('news', 'http://elcomercio.pe/feed/politica/actualidad.xml', 'nonattack')
# write_each_news('news', 'http://elcomercio.pe/feed/tecnologia.xml', 'nonattack')
# write_each_news('news', 'http://elcomercio.pe/feed/gastronomia.xml', 'nonattack')

# read_and_clean('news', '00', True)

# remove_first_line('00', 'txt')
#
tokenize_files('news/clean', '00/attack')

# rename_files('00/attack')
# rename_files('00/nonattack')
# rename_files('news/clean')
# rename_files('news/raw', 'html')

# write_each_news('http://elcomercio.pe/feed/lima/policiales.xml')
# print(datetime.datetime.now().strftime('%c')) #Wed May 11 16:30:06 2016
# geo_search_twitter('Surco', 'neighborhood', 'asalto', 'violacion')

