import random
import urllib.request
#from urllib import request

def download_web_page(url):
    name = random.randrange(1000)
    full_name = str(name) + ".jpg"
    urllib.request.urlretrieve(url, full_name)


def download_file(url, file_name):
    response = urllib.request.urlopen(url)
    data = response.read()
    data_str = str(data)
    lines = data_str.split("\\n")
    fx = open(file_name, "w")
    for line in lines:
        fx.write(line + "\n")
    fx.close()
