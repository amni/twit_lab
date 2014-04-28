
print "earliest possible test"
from tweepy import Stream
from tweepy import API
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from keys import *
print "pretest"

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
			user=User.query.filter_by(id=status.user_id).first()
			print ("User followers: %d" % user.followers_count)
			
		except:
			continue
		print ("Retweets: %d" % status.retweet_count)
		print

print(dir(status))
print(status.retweet_count)
