import tweepy
from tweepy.auth import OAuthHandler
import csv

def get_stuff(api,nombre=None):
    stuff = tweepy.Cursor(api.user_timeline, screen_name = nombre, include_rts = True)
    return stuff

def get_tweets(stuff, n):
    tweets=[]
    tweets2=[]
    for status in stuff.items(n):
        tweets.append(str(status.created_at)+","+ str(status.author.screen_name)+","+str(status.text)+","+"\n"+"\n")
        tweets2.append(str(status.created_at)+","+ str(status.author.screen_name)+","+str(status.text)+",")
    return tweets,tweets2

# def get_all_tweets(api,screen_name):
# 	#Twitter only allows access to a users most recent 3240 tweets with this method
#
# 	#authorize twitter, initialize tweepy
# 	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# 	auth.set_access_token(access_key, access_secret)
# 	api = tweepy.API(auth)
#
# 	#initialize a list to hold all the tweepy Tweets
# 	alltweets = []
#
# 	#make initial request for most recent tweets (200 is the maximum allowed count)
# 	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
#
# 	#save most recent tweets
# 	alltweets.extend(new_tweets)
#
# 	#save the id of the oldest tweet less one
# 	oldest = alltweets[-1].id - 1
#
# 	#keep grabbing tweets until there are no tweets left to grab
# 	while len(new_tweets) > 0:
#
# 		#all subsiquent requests use the max_id param to prevent duplicates
# 		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
#
# 		#save most recent tweets
# 		alltweets.extend(new_tweets)
#
# 		#update the id of the oldest tweet less one
# 		oldest = alltweets[-1].id - 1
#
# 	#transform the tweepy tweets into a 2D array that will populate the csv
# 	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]


	# #write the csv
	# with open('%s_tweets.csv' % screen_name, 'wb') as f:
	# 	writer = csv.writer(f)
	# 	writer.writerow(["id","created_at","text"])
	# 	writer.writerows(outtweets)
