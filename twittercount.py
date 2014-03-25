from tweepy import API
from tweepy import OAuthHandler
from keys import *
from time import sleep

import json 

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = API(auth)

with open('data.txt', 'r') as infile:
    statuses = infile.readlines()
    for status in statuses:
        load_stat = json.loads(status)
        print api.get_status(load_stat['id']).retweet_count
        print api.get_status(load_stat['id']).favorite_count
        sleep(10)