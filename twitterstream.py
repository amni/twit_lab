from tweepy import Stream
#from tweepy import API
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from keys import *
import sys

import json 

class listener(StreamListener):

    def on_status(self, status):
        stored_status={}
        if status.text:
            stored_status['text']= status.text
            stored_status['id']= status.id
            stored_status['favorite_count']= status.favorite_count
            stored_status['retweet_count']= status.retweet_count
            stored_status['created_at']= str(status.created_at)
            with open('data.txt', 'a') as outfile:
                json.dump(stored_status, outfile)
                outfile.write('\n')

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
#api = API(auth)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=['the'])