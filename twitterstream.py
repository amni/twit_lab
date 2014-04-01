from tweepy import Stream
#from tweepy import API
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from keys import *
import sys
import json
import database as db
Tweet = db.Tweet
User= db.User
session = db.session

class listener(StreamListener):

    def on_status(self, status):
        stored_status={}
        tweet_user=status.user
        if status.text:
            stored_status['text']= status.text
            stored_status['id']= status.id
            stored_status['favorite_count']= status.favorite_count
            stored_status['retweet_count']= status.retweet_count
            stored_status['created_at']= str(status.created_at)
            with open('data.txt', 'a') as outfile:
                user= User(id= tweet_user.id, followers_count=tweet_user.followers_count)
                if not session.query(User).filter_by(id=user.id).first():
                    session.add(user)
                # if "retweeted_status" in dir(status):
                #     print "retweet"
                if "retweeted_status" in dir(status): 
                    print "got retweet"
                    retweeted_tweet=session.query(Tweet).filter_by(text=status.text).first()
                    if retweeted_tweet:
                        retweeted_tweet.retweet_count+=1
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

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
#api = API(auth)
twitterStream = Stream(auth, listener())
twitterStream.sample()