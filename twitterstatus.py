from tweepy import Stream
from tweepy import API
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from keys import *

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = API(auth)

status = api.get_status(458140970580996096)

print(dir(status))
print(status.retweet_count)