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


def write_news_file(url):
    browser = webdriver.Firefox()
    browser.get(url)
    data_formatted = browser.page_source.encode('utf-8')
    browser.close()
    file_name = 'news_' + datetime.datetime.now().strftime('%d%m%y%H%M%S') + '.xml'
    f = open('News/' + file_name, 'wb')
    f.write(data_formatted)
    f.flush()
    f.close()


def write_each_news(url):
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
        file_name = news_url.split('/')[-1]
        try:
            news_element = driver.find_element_by_id('main-txt-nota')
        except NoSuchElementException:
            print('main-txt-nota not found on ' + file_name)
            continue
        news_content = news_element.get_attribute('innerHTML').encode('utf-8')
        content = fecha + "\n" + news_content.decode('utf-8')
        f = open('News/' + file_name + '.html', 'w')
        f.write(content)
        f.flush()
        f.close()
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
        f = open('News/' + file_name + '.html', 'wb')
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


def read_and_clean():
    weird_string = '&nbsp;'
    news = glob.glob("News/*.html")
    for news_file in news:
        print(news_file)
        file_name = 'CleanNews/' + news_file.split('/')[1].split('.')[0] + '.txt'
        if not os.path.isfile(file_name):
            rf = open(news_file, 'r')
            news_raw = rf.read()
            news_content = news_raw.split('<style')[0].split('<script')[0].replace(weird_string, " ")
            clean_content = clean_html(news_content)
            rf.flush()
            rf.close()
            print(clean_content)
            f = open(file_name, 'w')
            f.write(clean_content.strip())
            f.flush()
            f.close()


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def remove_tags(text):
    return ''.join(ET.fromstring(text).itertext())


def get_dates():
    news = glob.glob("News/*.html")
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
        with open("CleanNews/"+web_url+".txt", 'r') as clean_original:
            data = clean_original.read()
        with open("CleanNews/"+web_url+".txt", 'w') as clean_modified:
            clean_modified.write(fecha + "\n" + data)
    browser.close()


def remove_weird_character():
    weird_String = '&nbsp;'
    news = glob.glob("CleanNews/*.txt")
    for news_file in news:
        with open(news_file, 'r') as original:
            data = original.read()
        data.replace(weird_String, " ")
        with open(news_file, 'w') as modified:
            modified.write(data.replace(weird_String, " "))


# remove_weird_character()
read_and_clean()
# search_in_twitter('Surco', 'neighborhood', 'robo')
# write_news_file('http://elcomercio.pe/feed/lima/policiales.xml')
# write_each_news('http://elcomercio.pe/feed/lima/policiales.xml')
# print(datetime.datetime.now().strftime('%c')) #Wed May 11 16:30:06 2016
# geo_search_twitter('Surco', 'neighborhood', 'asalto', 'violacion')

