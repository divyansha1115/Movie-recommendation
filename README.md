# Movie-recommendation
The data set have been taken from [movieLens](http://files.grouplens.org/datasets/movielens/ml-latest-small.zip) and the movie information was extracted from [IMDB](https://www.imdb.com/).

## Getting Started
cd into any of the heroku directories
```
cd heroku
```
pip install all the requirements using 
```
pip install requirements.txt
```
Run the flask app
```
python app.py
```

## File Description
* scrape.py - Used tp scrape the IMDB data
* heroku - Contains the web app for movie recommendation using the **Matrix Factorization Method** -> (https://movie-recomm-1.herokuapp.com/)
* heroku2 - Contains the web app for movie recommendation using the **User based collaborative filtering** ->(https://movie-recomm-2.herokuapp.com/)
* heroku3 - Contains the web app for movie recommendation using the **Item based collaborative filtering**-> (https://movie-recomm-3.herokuapp.com/) 

>This has been deployed but is not working due to some server load issue but will work in localhost
> The ratings in the app should be an integer ranging from 0-5

## Deployment
The deployment of these apps has been done through [Heroku](https://signup.heroku.com/?c=7013A000000ib1xQAA&gclid=CjwKCAiA45njBRBwEiwASnZT5zB0BVGD6Y2OAPoLZpdVsn3tqrPG5Bop1k6u9Ooxst7c9dUG3ae0lhoCkx8QAvD_BwE)<br>
The database was stored using [Mlab](https://mlab.com/)

# Movie Lens Dataset Description

The small version of this dataset have been used which contains 100,000 ratings and 3,600 tag applications applied to 9,000 movies by 600 users.<br>
Only ~800 movies were used from this dataset due to server issues.<br>
We have used 3 files from this dataset

* ratings.csv - Each line of this file after the header row represents one rating of one movie by one user
* movies.csv -  Each line of this file after the header row represents one movie
* links.csv - Each line of this file after the header row represents one movie

