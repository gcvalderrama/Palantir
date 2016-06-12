# foods = ['food1', 'food2', 'food3', 'food4']
# for f in foods[:2]:
#     print(f)
#     print(len(f))
#
# for i in range(20):
#     print(i)
#
# for i in range(5, 20):
#     print(i)
#
# #starting, until what number, increment
# for i in range(5, 20, 3):
#     print(i)
#
# buttcrack = 3
#
# while buttcrack <= 5:
#     print(buttcrack)
#     buttcrack += 1
#
# magicNumber = 34
# '''
# for i in range(101):
#     if i is magicNumber:
#         print('We found the magic number')
# '''
#
# for i in range(101):
#     if i is magicNumber:
#         print(i, ' is the magic number')
#         break
#     else:
#         print(i)
#
#
# def download_main_page():
#     print('I\'m downloading it')
#
#
# def download_news(url='defaultUrl'):
#     return 'Downloading ' + url
#
#
# result = download_news()
# print(result)
#
#
# def add_numbers(*args):
#     total = 0
#     for i in args:
#         total += i
#     return total
#
#
# def health_calculator(age, apples_ate, cigarettes):
#     return (100-age) + (apples_ate * 3) - (cigarettes * 2)
#
#
# parameters = [31, 2, 0]
# print(health_calculator(*parameters)) #unpacking parameters
#
# total = add_numbers(1, 5, 6)
# print(total)
#
# classmates = {"Tony":"cool, but smells", "Cindy":"sits behind me", "Banner":"asks to many questions"}
# for k, v in classmates.items():
#     print(k + " " + v)

# import requests
# import lxml
# from bs4 import BeautifulSoup

# def trade_spider(url, max_pages):
#     page = 1
#     while page < max_pages:
#         # url = url + page
#         source_code = requests.get(url)
#         plain_text = source_code.text
#         soup = BeautifulSoup(plain_text)
# class Child(Parent):

#
# class WebCrawler:
#     #def __init__(self):
#
#
#     def elcomercio_spider(url):
#         try:
#             source_code = requests.get(url)
#             plain_text = source_code.text
#             soup = BeautifulSoup(source_code,"lxml")
#             for link in soup.findAll('a'):
#                 href = link.get('href')
#                 print(href)
#         except TypeError:
#             print('catching type error')


# elcomercio_spider('http://elcomercio.pe/feed/lima/policiales.xml')

fw = open("sample.txt", "w")
fw.write("writing some stuff here\n")
fw.write("I like bacon\n")
fw.close()

fr = open("sample.txt", "r")
text = fr.read()
fr.close()
print(text)
