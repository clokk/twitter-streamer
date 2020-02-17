from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json

import twitter_credentials

def retweet_check(status):
	if hasattr(status, 'retweeted_status'):
		if status.user.id == "260865201":
			return True
		else:
			return False
	else:
		return False

def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True

def get_Text(tweet):
	try:
		return tweet.extended_tweet['full_text']
	except AttributeError as e:
		return tweet.text

def message_slack(text):
	from urllib import request, parse

	post = {"text": "{0}".format(text)}

	try:
		json_data = json.dumps(post)
		req = request.Request("slack_API_key_here",
			data=json_data.encode('ascii'),
			headers={'Content-Type': 'application/json'})
		resp = request.urlopen(req)
	except Exception as em:
		print("EXCEPTION: " + str(em))

class TwitterClient():
	def __init__(self, twitter_user=None):
		self.auth = TwitterAuth().authenticate_twitter_app()
		self.twitter_client = API(self.auth)

		self.twitter_user = twitter_user

	def get_user_timeline_tweets(self, num_tweets):
		tweets = []
		for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
			tweets.append(tweet)
		return tweets

	def get_friend_list(self, num_friends):
		friend_list = []
		for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
			friend_list.append(friend)
		return friend_list

	def get_home_timeline_tweets(self, num_tweets):
		home_timeline_tweets = []
		for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
			home_timeline_tweets.append(tweet)
		return home_timeline_tweets

class TwitterAuth():

	def authenticate_twitter_app(self):
		auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
		auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
		return auth



class TwitterStreamer():
	"""
	class for streaming and processing live tweets.
	"""

	def __init__(self):
		self.twitter_auth = TwitterAuth()

	def stream_tweets(self, user_id):
		#this handles connection to the Twitter Streaming API.

		listener = TwitterListener()
		auth = self.twitter_auth.authenticate_twitter_app()
		stream = Stream(auth, listener)

		stream.filter(follow=[user_id])
		# stream.filter(track=['api','collusion'])

class TwitterListener(StreamListener):
	"""
	basic listener class that just prints received tweets to stdout.
	"""

	# def __init__(self):
		# self.fetched_tweets_filename = fetched_tweets_filename

	def on_status(self, status):
		if str(status.user.id) == "25073877":
			text = ""
			text = get_Text(status)
			print(text)
			message_slack(text)
			text_lower = text.lower()

			if 'sanctuary' in text_lower:
				print('success') 
				message_slack("sanctuary + 1")

			if 'mueller' in text_lower:
				print('success')
				message_slack("Mueller + 1")
				return True
		return True

		# if from_creator(status):
		# 	# Prints out the tweet
		# 	text = get_Text(status)
		# 	print(text)
		# 	message_slack(text)
		# 	text_lower = text.lower()

		# 	if 'collusion' in text_lower:
		# 		print('success') 
		# 		message_slack("collusion + 1")

		# 	if 'mexico' in text_lower:
		# 		print('success')
		# 		message_slack("Mexico + 1")
		# 		return True

		# if retweet_check(status):
		# 	# print(status)
		# 	text = get_Text(status)
		# 	print(text)
		# 	message_slack(text)
		# 	text_lower = text.lower()
		# 	if 'collusion' in text_lower:
		# 		print('success') 
		# 		message_slack("collusion + 1")

		# 	if 'mexico' in text_lower:
		# 		print('success')
		# 		message_slack("Mexico + 1")
		# 		return True
		# return True


	# def on_data(self, data):
	# 	print(data)
	# 	print("___________________________")
	# 	json_data = json.loads(data)
	# 	text = json_data["text"].lower()
	# 	print(text)

	# 	if 'collusion' in text:
	# 		print('success') 
	# 		message_slack("collusion + 1")

	# 	if 'mexico' in text:
	# 		print('success')
	# 		message_slack("Mexico + 1")

	# 	return True
	###################################
		# 	with open(self.fetched_tweets_filename, 'a') as tf:
		# 		tf.write(data)
		# 	return True
		# except BaseException as e:
		# 	print("Error on_data: %s" % str(e))
		# return True


	def on_error(self, status):
		if status == 420:
			# Returning False on_data in case rate limit occurs.
			return False
		print(status)
		


if __name__ == "__main__":

	hash_tag_list = ["donald trump", "bernie sanders"]
	fetched_tweets_filename = "tweets.json"

	user_id_donald = "25073877"

	user_id_csleisz = "260865201"

	# twitter_client = TwitterClient('realDonaldTrump')
	# print(twitter_client.get_user_timeline_tweets(1))

	twitter_streamer = TwitterStreamer()
	twitter_streamer.stream_tweets(user_id_donald)
