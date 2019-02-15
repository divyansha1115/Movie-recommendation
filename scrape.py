import pandas as pd
import time
import csv
def find_data(page_url):
    import urllib.request
    from bs4 import BeautifulSoup, NavigableString
    import json
    from requests import get
    from urllib.request import Request, urlopen
    response = get(page_url)
    html_soup = BeautifulSoup(response.text,'html.parser')
    for script in html_soup(["script", "style"]):
        script.decompose()
    try:
        #thumbnail
        movie_containers = html_soup.find_all('div', class_ = 'slate_wrapper')
        movie = movie_containers[0]
        img = movie.div.a.img['src']
    except:
        img = ''
    try:
        #rating
        movie_containers = html_soup.find_all('div', class_ = 'ratings_wrapper')
        movie = movie_containers[0]
        rating = movie.div.strong.text
    except:
        rating = ''
    try:
        #year
        movie_containers = html_soup.find_all('div', class_ = 'title_wrapper')
        movie = movie_containers[0]
        year = movie.h1.a.text
    except:
        rating = ''
    try:
        #summary
        movie_containers = html_soup.find_all('div', class_ = 'inline canwrap')
        movie = movie_containers[0]
        summary = movie.text.replace('\n','')
        summary = summary.replace('\t','')
    except:
        summary = ''
    
        
    data = {
        'img':img,
        'rating':rating,
        'year':year,
        'summary':summary,
    }
    return data
df1 = pd.read_csv("ml-latest-small/links.csv")
df2 = pd.read_csv("ml-latest-small/movies.csv")

imdb_id = df1['imdbId']


extracted_data = []
f = csv.writer(open('scrapped.csv', 'w'))
f.writerow(['Thumbnail', 'Rating','Year','Summary','Title','MovieId'])
imdbID = df1['imdbId']
i=0
for imdbID in imdbID:
    url = 'https://www.imdb.com/title/tt0'+ str(imdbID)
    print('Extracting data from %s'%url)
    #Lets wait for 5 seconds before we make requests, so that we don't get blocked while scraping. 
    #if you see errors that say HTTPError: HTTP Error 429: Too Many Requests , increase this value by 1 second, till you get the data. 
    try:
        extracted_data.append(find_data(url))
        data = find_data(url)
    except:
        print('wait')
        time.sleep(100)
        
        try:
            url = url+str(0)
            extracted_data.append(find_data(url))
            print('Extracting data from %s'%url)
            data = find_data(url)
        except:
            i=i+1
            continue
        
    Title = df2['title'][i]
    MovieId =  df2['movieId'][i]
    Thumbnail = data['img']
    Rating = data['rating']
    Year = data['year']
    Summary = data['summary']
    f.writerow([Thumbnail,Rating,Year,Summary,Title,MovieId])
    print(Rating)
    i=i+1


