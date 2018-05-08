"""
Python Script to extract the image from yts.ag
"""

from bs4 import BeautifulSoup
import requests
import xlwt

movie_list = []

for i in range(1, 10):
    source = (requests.get("https://yts.me/browse-movies?page={}".format(i)).text)

    soup = BeautifulSoup(source, 'lxml')

    for a in soup.find_all('div', class_='browse-movie-wrap'):
        content_image = a.find('a', class_='browse-movie-link')
        content_title = a.find('a', class_='browse-movie-title')
        image = content_image.img['src']
        title = content_title.text

        web_content = {"title": title, "image": image}
        movie_list.append(web_content)

book = xlwt.Workbook()
sheet1 = book.add_sheet("sheet")
sheet1.write(0, 0, "Title")
sheet1.write(0, 1, "Image")

r = 0

for movie in movie_list:
    r += 1
    sheet1.write(r, 0, movie['title'])
    sheet1.write(r, 1, movie['image'])


book.save("sample.xls")