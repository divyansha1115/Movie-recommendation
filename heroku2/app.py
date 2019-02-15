from flask import Flask, render_template,request,url_for
from math import sqrt
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
	for i in range(1,50):
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
			movieId.append(int(x))
			ratings.append(result[x])
		#find numbber of non zero elements
		# count = 0
		# for i in ratings:
		# 	if i!= '':
		# 		count=count+1
		#replace empty with zero and convert rest to int
		a=0;
		for i in ratings:
			if i == '':
				ratings[a]=0
			else:
				ratings[a] = int(i)

			a=a+1
		#calculate avg of number of rated
		# avg = sum(ratings)/count
		# a=0;
		# #replace the 0 ones with avg
		# for i in ratings:
		# 	if i == 0:
		# 		ratings[a]=avg
		# 	a=a+1

		
	

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
		
					

		def pearson_correlation(userId1,userId2):

		    # To get both rated movies
		    both_rated = {}
		    for movie in user_movie[userId1]:
		        if movie in user_movie[userId2]:
		            both_rated[movie] = 1

		    number_of_ratings = len(both_rated)		
		    
		    # Checking for number of ratings in common
		    if number_of_ratings == 0:
		        return 0
		    userId1_preferences_sum = sum([user_movie[userId1][movie] for movie in both_rated])
		    userId2_preferences_sum = sum([user_movie[userId2][movie] for movie in both_rated])
		    userId1_square_preferences_sum = sum([pow(user_movie[userId1][movie],2) for movie in both_rated])
		    userId2_square_preferences_sum = sum([pow(user_movie[userId2][movie],2) for movie in both_rated])
		    product_sum_of_both_users = sum([user_movie[userId1][movie] * user_movie[userId2][movie] for movie in both_rated])
		    numerator = product_sum_of_both_users - (userId1_preferences_sum*userId2_preferences_sum/number_of_ratings)
		    denominator = sqrt((userId1_square_preferences_sum - pow(userId1_preferences_sum,2)/number_of_ratings) * (userId2_square_preferences_sum -pow(userId2_preferences_sum,2)/number_of_ratings))
		    if denominator == 0:
		        return 0
		    else:
		        r = numerator/denominator
		        return r 


	
	    
		def user_reommendations(user):

		    totals = {}
		    simSums = {}
		    rankings_list =[]
		    for other in user_movie:
		        if other == user:
		            continue
		        similarity = pearson_correlation(user,other)
		        if similarity <=0: 
		            continue
		        for movie in user_movie[other]:
		            if movie not in user_movie[user] or user_movie[user][movie] == 0:
		                totals.setdefault(movie,0)
		                totals[movie] += user_movie[other][movie]* similarity
		                # sum of similarities
		                simSums.setdefault(movie,0)
		                simSums[movie]+= similarity
		    rankings = [(total/simSums[movie],movie) for movie,total in totals.items()]
		    rankings.sort()
		    rankings.reverse()
		    recommendataions_list = [recommend_movie for score,recommend_movie in rankings]
		    return recommendataions_list[:10] 
		df = pd.merge(df3, df2, on='movieId')
		df1 = df[['userId','title','rating']]
		dict1 =df1.groupby('userId')[['title','rating']].apply(lambda g: g.values.tolist()).to_dict()
		for key in dict1:
			dict1[key]=dict(dict1[key])
		user_movie = dict1
		result = predictions = user_reommendations(userId)

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
