from flask import Flask, render_template,request,url_for
import pandas as pd
from pymongo import MongoClient
app = Flask(__name__)
import random


client = MongoClient("mongodb+srv://divyansha1115:papamumma1115@cluster0-znlly.mongodb.net/test?retryWrites=true")
db = client.app
collection1 = db.moviesf
collection2 = db.imdbf




@app.route('/')
def home():	
	def get_random_doc():
		count = collection2.count()
		return collection2.find()[random.randrange(count)]
	title = []
	for i in range(1,10):
		name = get_random_doc()
		title.append(name)

		
	return render_template('home.html' , title = title)


@app.route('/predict', methods=['POST'])
def predict():
	df2 = pd.read_csv("ml-latest-small/moviesf.csv")
	df3 = pd.read_csv("ml-latest-small/ratingsf.csv")
	df3 = df3.drop(df3.columns[0], axis=1)
	df2 = df2.drop(df2.columns[0], axis=1)
	# find the mean of each user
	if request.method == 'POST':
		user_group = df3.groupby(by='userId')
		user_means = user_group['rating'].agg(['mean', 'count'])
		# create a new column named "meanCenteredRating"
		# this function takes in ratings of one user and return mean_centered ratings of that user
		mean_centering = lambda ratings: ratings - ratings.mean()
		df3['meanCenteredRating'] = user_group['rating'].transform(mean_centering)
		df_mean = pd.merge(df3, df2, on='movieId')
		def recommend_user(user_rating,movie_matrix):
		    corrMatrix = movie_matrix.corr(method='pearson', min_periods=10)
		    similar_candidates = pd.Series()
		    for i in range(0, len(user_rating.index)):
		        # retrieve similar movies to this one that I rated
		        similar_movies = corrMatrix[user_rating.index[i]].dropna()
		        # scale its similarity by how well I rated this movie
		        similar_movies = similar_movies.map(lambda x: x * user_rating[i])
		        # add the score to the list of similar candidates
		        similar_candidates = similar_candidates.append(similar_movies)
		    similar_candidates.sort_values(inplace = True, ascending = False)
		    similar_candidates = similar_candidates.groupby(similar_candidates.index).sum()
		    similar_candidates.sort_values(inplace = True, ascending = False)
		    return similar_candidates.head(10)


		movie_matrix_normalazied = df_mean.pivot_table(index='userId', columns='title', values='meanCenteredRating')
		#retrieve ratings and normalized them and convert them into pandas series
		result = request.form.to_dict()
		title = []
		ratings = []
		for x in result:
			title.append(x[:-1])
			ratings.append(result[x])
		a=0
		count = 0
		#find numbber of non zero elements
		for i in ratings:
			if i!= '':
				count=count+1

		#replace empty with zero and convert rest to int
		for i in ratings:
			if i == '':
				ratings[a]=0
			else:
				ratings[a] = int(i)

			a=a+1
		#calculate avg of number of rated
		avg = sum(ratings)/count
		a=0;
		#normalise all the ratings and replace the 0 ones with avg
		for i in ratings:
			ratings[a]=avg - ratings[a]
			a=a+1

		# return render_template("result2.html",title = title,ratings=ratings)

		df=pd.DataFrame(ratings,index=title)
		series = df.iloc[:,0]
		myRatings_normalazied = series
		#return render_template("result2.html",title = myRatings_normalazied)

		ans = recommend_user(myRatings_normalazied,movie_matrix_normalazied)
		#ratings = ans.tolist()	
		result = ans.index.tolist()
		title = []
		def doc_info(obj):
			for y in obj:
				return dict(y)
		for x in result:
			myquery = { "Title": x }
			mydoc = collection2.find(myquery)
			title.append(doc_info(mydoc))
			
		return render_template("result3.html",title = title )


		#end code
		
		



if __name__ == '__main__':
    app.debug = True
    app.run()









