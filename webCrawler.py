import datetime
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from twitter import *
from urllib import *
from pprint import pprint

def write_news_file(url):
    browser = webdriver.Firefox()
    browser.get(url)
    data_formatted = browser.page_source.encode('utf-8')
    browser.close()
    file_name = 'news_' + datetime.datetime.now().strftime('%d%m%y%H%M%S') + '.xml'
    #data_formatted = news_content.decode('utf-8')#.encode('cp850', 'replace').decode('cp850')
    f = open('Noticias/' + file_name, 'wb')
    f.write(data_formatted)
    f.flush()
    f.close()


def write_each_news(url):
    browser = webdriver.Firefox()
    browser.get(url)
    list_linker_href = browser.find_elements_by_xpath('//xhtml:a[@href]')
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
        f = open('Noticias/' + file_name + '.html','wb')
        f.write(datetime.datetime.now().strftime('%c') + '\n')
        f.write(news_content)
        f.flush()
        f.close()
    browser.close()
    driver.close()


def geo_search_twitter(location, granularity, *args):
    t_client = Twitter(
        auth=OAuth('228157926-JbzXfMmj8N8dWPTZfJBQc7KGp6VGBecOnfs8hzmo',
                   'bGN6fu9ENRuM0b3PYbNobdR7zAvlsimHc6C1J2dbrERWt',
                   'MkPdpJrKYW7ObGO73n1RoPQfH',
                   'No06OWAsIkeMnUPx0Tzrqkm6JjcfAUvyO4UD5Sw3kEYJGOydyB'))
    res_location = t_client.geo.search(query=location, granularity=granularity)
    place_id = res_location['result']['places'][0]['id']

    urllib.urlencode(query_args)
    result = t.search.tweets(q="place:%s" % place_id)
    for tweet in result['statuses']:
        print tweet


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
    # json_data = json.loads(result)
    # pprint(json_data)
    for tweet in result['statuses']:
        print(tweet['text'] + " | " + tweet['place']['name'] if tweet['place'] else "Undefined place")
    # response = twitter_client.search.tweets(q="#pycon")
    # print(response)
    # for key in args:
    #     print(key)


search_in_twitter('Surco', 'neighborhood', 'robo')
#write_news_file('http://elcomercio.pe/feed/lima/policiales.xml')
#write_each_news('http://elcomercio.pe/feed/lima/policiales.xml')
#print(datetime.datetime.now().strftime('%c')) #Wed May 11 16:30:06 2016
geo_search_twitter('Surco', 'neighborhood', 'asalto', 'violacion')

