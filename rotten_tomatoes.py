from bs4 import BeautifulSoup
import requests
import json
import xlwt
import copy

RT_BASE_URL = "https://www.rottentomatoes.com"

top_rated_movies = []

page = 1

while True:
    url = "https://www.rottentomatoes.com/api/private/v2.0/browse?minTomato=83&maxTomato=100&maxPopcorn=100&services" \
          "=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=1;2;4;5;6;9;10;11;13;18;14&certified" \
          "&sortBy=release&type=dvd-streaming-all&page={}"

    url = url.format(page)
    print(url)

    source = requests.get(url).json()

    results = source['results']

    if len(results) == 0:
        break

    pop_filter = filter(lambda x: int(x['popcornScore']) > 84, results)
    pop_filter_list = copy.deepcopy(list(pop_filter))

    for r in pop_filter_list:
        movie = {"title": r['title'], "link": RT_BASE_URL + r['url'], "popcornScore": r['popcornScore'],
                 "tomatoScore": r['tomatoScore']}
        top_rated_movies.append(movie)

    print("Page - " + str(page) + " Completed")
    page += 1


print("No of top rated movies --- " + str(len(top_rated_movies)))

book = xlwt.Workbook()
sheet1 = book.add_sheet("sheet")
sheet1.write(0, 0, "Title")
sheet1.write(0, 1, "PopCorn Score")
sheet1.write(0, 2, "TomatoMetre Score")
sheet1.write(0, 3, "Link")

r = 0

for movie in top_rated_movies:
    r += 1
    sheet1.write(r, 0, movie['title'])
    sheet1.write(r, 1, movie['popcornScore'])
    sheet1.write(r, 2, movie['tomatoScore'])
    sheet1.write(r, 3, movie['link'])

book.save("/Users/kishore/Documents/movies.xls")