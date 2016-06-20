import datetime
import xml.etree.ElementTree as ET
import glob
import re
import os.path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from twitter import *
from bs4 import BeautifulSoup
import os

chromedriver = "/Users/ozo/ExternalDemo/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver


def write_each_news(url, tag):
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
        with open("News/" + file_name + ".html", 'w') as file:
            file.write(content)
    browser.close()
    driver.close()


def read_and_clean(origin, destination, skip_validation):
    news = glob.glob(origin + "/*.html")
    for news_file in news:
        print(news_file)
        file_name = destination + '/' + news_file.split('/')[1].split('.')[0] + '.txt'
        if skip_validation or not os.path.isfile(file_name):
            with open(news_file, 'r') as rf:
                news_raw = rf.read()
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


def rename_files():
    news = glob.glob("News/*.html")
    for news_file in news:
        if "?ref_bajada" in news_file:
            updated_news_file = news_file.replace('?ref_bajada', '')
            os.rename(news_file, updated_news_file)
            news_file = updated_news_file

        if news_file.startswith("News/actualidad--") or news_file.startswith("News/gastronomia--") or \
            news_file.startswith("News/policiales--") or news_file.startswith("News/tecnologia--"):
            continue
        os.rename(news_file, news_file.replace('News/', 'News/policiales--'))


read_and_clean('News', 'CleanNews', True)

# remove_weird_character()
# read_and_clean('News', 'corporaNews', True)
# search_in_twitter('Surco', 'neighborhood', 'robo')

# rename_files()

# write_each_news('http://elcomercio.pe/feed/lima/policiales.xml', 'policiales')
# write_each_news('http://elcomercio.pe/feed/politica/actualidad.xml', 'actualidad')
# write_each_news('http://elcomercio.pe/feed/tecnologia.xml', 'tecnologia')
# write_each_news('http://elcomercio.pe/feed/gastronomia.xml', 'gastronomia')

# print(datetime.datetime.now().strftime('%c')) #Wed May 11 16:30:06 2016
