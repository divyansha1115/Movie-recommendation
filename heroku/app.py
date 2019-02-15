from flask import Flask, render_template,request,url_for
import pandas as pd
from pymongo import MongoClient
import csv
app = Flask(__name__)
import random
import numpy as np
from scipy.sparse.linalg import svds

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

		
	return render_template('home3.html' , title = title)


@app.route('/predict', methods=['POST'])
def predict():
	
	userId = 610
	if request.method == 'POST':
		userId = userId+1
		result = request.form.to_dict()
		movieId = []
		ratings = []
		for x in result:
			movieId.append(int(x[:-1]))
			ratings.append(result[x])
		#find numbber of non zero elements
		count = 0
		for i in ratings:
			if i!= '':
				count=count+1
		#replace empty with zero and convert rest to int
		a=0;
		for i in ratings:
			if i == '':
				ratings[a]=0
			else:
				ratings[a] = int(i)

			a=a+1
		#calculate avg of number of rated
		avg = sum(ratings)/count
		a=0;
		#replace the 0 ones with avg
		for i in ratings:
			if i == 0:
				ratings[a]=avg
			a=a+1

		
	

	# with open('ml-latest-small/ratings.csv.csv', 'a') as newFile:
	#     newFileWriter = csv.writer(newFile)
	#     for i in range(len(movieId)):
	#     	newFileWriter.writerow([userId,movieId[i],ratings[i],'not_def'])

	df2 = pd.read_csv("ml-latest-small/moviesf.csv")
	df3 = pd.read_csv("ml-latest-small/ratingsf.csv")
	df3 = df3.drop(df3.columns[0], axis=1)
	df2 = df2.drop(df2.columns[0], axis=1)

	for i in range(len(movieId)):
		l = [userId,movieId[i],ratings[i],0]
		df5 = pd.DataFrame([l],columns=['userId','movieId','rating','timestamp'])
		
		df3= pd.concat([df3,df5])
		df3 = df3.reset_index(drop=True)
	
	df = pd.merge(df3, df2, on='movieId')
	movieId_matrix = df.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)
	movieId = movieId_matrix.as_matrix()
	user_ratings_mean = np.mean(movieId, axis = 1)
	movieId_demeaned = movieId - user_ratings_mean.reshape(-1, 1)
	U, sigma, Vt = svds(movieId_demeaned, k = 50)
	sigma = np.diag(sigma)
	all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
	preds_df = pd.DataFrame(all_user_predicted_ratings, columns = movieId_matrix.columns)

	def recommend_movies(predictions_df, userId, movies_df, original_ratings_df, num_recommendations=5):
    
	    # Get and sort the user's predictionsss
	    user_row_number = userId - 11 # UserID starts at 1, not 0
	    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)
	    
	    # Get the user's data and merge in the movie information.
	    user_data = original_ratings_df[original_ratings_df.userId == (userId)]
	    user_full = (user_data.merge(movies_df, how = 'left', left_on = 'movieId', right_on = 'movieId').
	                     sort_values(['rating'], ascending=False)
	                 )

	    print ('User {0} has already rated {1} movies.'.format(userId, user_full.shape[0]))
	    print ('Recommending the highest {0} predicted ratings movies not already rated.'.format(num_recommendations))
	    
	    # Recommend the highest predicted rating movies that the user hasn't seen yet.
	    recommendations = (movies_df[~movies_df['movieId'].isin(user_full['movieId'])].
	         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
	               left_on = 'movieId',
	               right_on = 'movieId').
	         rename(columns = {user_row_number: 'Predictions'}).
	         sort_values('Predictions', ascending = False).
	                       iloc[:num_recommendations, :-1]
	                      )

	    return user_full, recommendations

	already_rated, predictions = recommend_movies(preds_df, userId, df2, df3,)

	result = predictions['title'].tolist()
	

	title = []
	def doc_info(obj):
		for y in obj:
			return dict(y)
	for x in result:
		myquery = { "Title": x }
		mydoc = collection2.find(myquery)
		title.append(doc_info(mydoc))



	return render_template("result3.html",title = title )

		










if __name__ == '__main__':
    app.debug = True
    app.run()
