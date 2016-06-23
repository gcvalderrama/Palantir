"""
This script extract news information from the local web
"""
import glob
import os
import os.path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class Crawler:

    def extract_web_news(self, folder, url, tag):
        """
        Extract information from the elcomercio feed url (XML format) and download them
         to a filepath
        :param folder: Folder where the news files will be saved
        :param url: feed url like http://elcomercio.pe/feed/lima/policiales.xml
        :param tag: news type like 'policiales'
        :return: void
        """
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

    def clean_raw_news(self, origin, destination, skip_validation):
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


