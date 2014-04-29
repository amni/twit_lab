from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from keys import *
import sys
import json

# Connect to DB
import database as db
Tweet = db.Tweet
User= db.User
session = db.session

class listener(StreamListener):

    def on_status(self, status):
        stored_status={}
        tweet_user=status.user
        if status.text:
            status.text = status.text.encode('ascii', 'ignore')
            stored_status['text']= status.text
            stored_status['id']= status.id
            stored_status['favorite_count']= status.favorite_count
            stored_status['retweet_count']= status.retweet_count
            stored_status['created_at']= str(status.created_at)
            with open('data.txt', 'a') as outfile:
                # Store user of tweet if not existing already
                user= User(id= tweet_user.id, followers_count=tweet_user.followers_count)
                if not session.query(User).filter_by(id=user.id).first():
                    session.add(user)
                    session.commit()
                # Add 1 to retweet count if tweet already exists
                if "retweeted_status" in dir(status): 
                    print "got retweet"
                    retweeted_tweet=session.query(Tweet).filter_by(text=status.text).first()
                    if retweeted_tweet:
                        retweeted_tweet.retweet_count+=1
                # Otherwise store tweet
                else: 
                    print "got tweet"
                    tweet = Tweet(tid=status.id, text=status.text, favorite_count=status.favorite_count, 
                                    retweet_count=status.retweet_count, created_at=status.created_at, user_id=tweet_user.id)
                    session.add(tweet)
                session.commit()
                json.dump(stored_status, outfile)
                outfile.write('\n')

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True

# Prepare filter parameters
f = open('popword.txt', 'r')
words = list()
for line in f:
    words.append(line.rstrip())

# Setup Streaming Client
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

# Start streaming
twitterStream.filter(track=words[:400], languages=["en"])