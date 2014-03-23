from tweepy import Stream
#from tweepy import API
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from keys import *

import json 

class listener(StreamListener):

    def on_data(self, data):
    	"""write tweet in the form of a json object everytime tweet data is received"""
    	loaded_data= json.loads(data)
    	stored_data={}
    	if 'text' in loaded_data:
    		stored_data['text']= loaded_data['text']
    		stored_data['id']= loaded_data['id']
    		stored_data['created_at']= loaded_data['created_at']
    		with open('data.txt', 'a') as outfile:
  				json.dump(stored_data, outfile)
  				outfile.write('\n')
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
#api = API(auth)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=['the'])