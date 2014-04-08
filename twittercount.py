from tweepy import API
from tweepy import OAuthHandler
from keys import *
from time import sleep

import json 
import database as db
Tweet = db.Tweet
session = db.session

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = API(auth)

tweets = session.query(Tweet).all()
for tweet in tweets:
    tweet.retweet_count = api.get_status(tweet.tid).retweet_count
    tweet.favorite_count = api.get_status(tweet.tid).favorite_count
    print tweet.retweet_count, tweet.favorite_count
    session.commit()
    sleep(10)

