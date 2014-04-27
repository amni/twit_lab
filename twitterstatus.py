from tweepy import Stream
from tweepy import API
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from keys import *

import database as db
Tweet = db.Tweet
User= db.User
session = db.session


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = API(auth)


tweets = session.query(Tweet).limit(100)

for tweet in tweets:
	if tweet.tid:
		try: 
			status = api.get_status(int(tweet.tid))
		except:
			continue
		print status.retweet_count
		count+=1

print(dir(status))
print(status.retweet_count)
