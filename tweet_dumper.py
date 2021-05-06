
# This code works well under good internet conditions

import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials


class Retriever():
	def __init__(self):
		self.consumer_key = "v6RhqOrvi0y59QvTgEdtcUd5J"
		self.consumer_secret = "HLEhJ3hRvfSLfXNY7kEWPXaUUf56lffmIcgx62pLoP6Wj03NqN"
		self.access_key = "2472634891-3Tm6kG0BbcbkagOz1DpuSlXIYPZYcJEqRt5rO0A"
		self.access_secret = "yNYmEK3KTlCr5adSVT73KXc0DwkRst6r35tVlaIjiO7d5"
				
	def get_all_tweets(self,screen_name):
		
		# Twitter only allows access to a users most recent 3240 tweets with this method
		
		# This limit can be exceeded if we buy the premium twitter API key.
		# P.S.  The source is not so credible
		
		
		#authorize twitter, initialize tweepy
		auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_key, self.access_secret)
		api = tweepy.API(auth)
		
		#initialize a list to hold all the tweepy Tweets
		alltweets = []	
		
		#make initial request for most recent tweets (200 is the maximum allowed count)
		new_tweets = api.user_timeline(screen_name = screen_name,count=200)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		#keep grabbing tweets until there are no tweets left to grab
		while len(new_tweets) > 0:
			print("getting tweets before ",oldest)
			
			#all subsiquent requests use the max_id param to prevent duplicates
			new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
			
			#save most recent tweets
			alltweets.extend(new_tweets)
			
			#update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1
			
			print(len(alltweets),"tweets downloaded so far" )
			# if len(alltweets) > 500:
			# 	break
		
		#transform the tweepy tweets into a 2D array that will populate the csv	
		outtweets = [tweet.text for tweet in alltweets]
		
		#write the csv	
		# with open('tweet/%s_tweets.csv' % screen_name, 'w') as f:
		# 	writer = csv.writer(f)
		# 	writer.writerow(["id","created_at","text"])
		# 	writer.writerows(outtweets)
		return outtweets


if __name__ == '__main__':
		#pass in the username of the account you want to download
	data = Retriever()
	data.get_all_tweets("elonmusk")
