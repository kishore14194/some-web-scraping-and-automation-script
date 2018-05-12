"""
Python Script to extract the image from monkey user and save in a Directory
"""

from bs4 import BeautifulSoup
import requests
import urllib.request as req
import os

MONKEY_USER_BASE_URL = "http://www.monkeyuser.com"

BASE_DIR_PATH = "/Users/kishore/Documents/Monkey_User_Comics/"

DIR_PATH = "/Users/kishore/Documents/Monkey_User_Comics/{}.png"

source = requests.get(MONKEY_USER_BASE_URL + "/toc/").text

soup = BeautifulSoup(source, 'lxml')

link_list = []

image_list = []

for a in soup.find_all('div', class_='page'):
    all_link = a.find_all('a')
    for link in all_link:
        blog_link = link['href']
        link_list.append(blog_link)

for lin in link_list:
    image_url = MONKEY_USER_BASE_URL + lin
    img_source = requests.get(image_url).text
    img_soup = BeautifulSoup(img_source, 'lxml')

    image_name = image_url.split('/')
    image_name = image_name[-2]

    img_content = img_soup.find("meta", property="og:image")
    image = img_content["content"] if img_content else False

    if image:

        is_existing_file = lambda x: True if image_name + ".png" in os.listdir(BASE_DIR_PATH) else False

        if is_existing_file:
            print("Already exists - " + image_name)
            continue

        try:
            req.urlretrieve(image, DIR_PATH.format(image_name))
            print("Image saved - " + image_name)
        except:
            print("Image ignored - " + image_name)
            continue

print("============Completed=============")
