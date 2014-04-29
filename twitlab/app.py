'''
    twitter
    -------

    A simple Flask demo app that shows how to login with Twitter via rauth.

    Please note: you must do `from twitter import db; db.create_all()` from
    the interpreter before running this example!
'''

from flask import (Flask, flash, request, redirect, render_template, session,
                url_for)
from flask.ext.sqlalchemy import SQLAlchemy

from rauth.service import OAuth1Service
from rauth.utils import parse_utf8_qsl
import json
import operator
import datetime
from dateutil import parser
import numpy
from nltk.corpus import stopwords


# Flask config
SQLALCHEMY_DATABASE_URI = 'sqlite:///twitter.db'
SECRET_KEY = '\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16'
DEBUG = True
TW_KEY = 'oZSbVzKCeyAZTDxw1RKog'
TW_SECRET = 'TuNoqA6NzEBS3Zrb8test7bxQfKTlBfLTXsZ8RaKAo'

# Flask setup
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

# rauth OAuth 1.0 service wrapper
twitter = OAuth1Service(
    name='twitter',
    consumer_key=TW_KEY,
    consumer_secret=TW_SECRET,
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    base_url='https://api.twitter.com/1.1/')


# models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    fb_id = db.Column(db.String(120))

    def __init__(self, username, fb_id):
        self.username = username
        self.fb_id = fb_id

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def get_or_create(username, fb_id):
        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User(username, fb_id)
            db.session.add(user)
            db.session.commit()
        return user


# views
@app.route('/')
def index():
    return render_template('login.html')


@app.route('/twitter/login')
def login():
    oauth_callback = url_for('authorized', _external=True)
    params = {'oauth_callback': oauth_callback}

    r = twitter.get_raw_request_token(params=params)
    data = parse_utf8_qsl(r.content)

    session['twitter_oauth'] = (data['oauth_token'],
                                data['oauth_token_secret'])
    return redirect(twitter.get_authorize_url(data['oauth_token'], **params))


@app.route('/twitter/authorized')
def authorized():
    request_token, request_token_secret = session.pop('twitter_oauth')

    # check to make sure the user authorized the request
    if not 'oauth_token' in request.args:
        flash('You did not authorize the request')
        return redirect(url_for('index'))

    try:
        creds = {'request_token': request_token,
                'request_token_secret': request_token_secret}
        params = {'oauth_verifier': request.args['oauth_verifier']}
        sess = twitter.get_auth_session(params=params, **creds)
    except Exception, e:
        flash('There was a problem logging into Twitter: ' + str(e))
        return redirect(url_for('index'))

    verify = sess.get('account/verify_credentials.json',
                    params={'format':'json'}).json()

    params = {'include_rts': 0,  # Include retweets
          'count': 100000}       # 10 tweets

    r = sess.get('statuses/user_timeline.json', params=params)

    messages={}
    tweets=[]
    retweet_count_map={}
    followers=0
    primetime_tweets=0
    nonprimetime_tweets=0
    picture_url=""
    for i, tweet in enumerate(r.json(), 1):
        picture_url= tweet["user"]["profile_image_url"]
        if "retweeted_status" not in tweet: 
            retweet_count= tweet['retweet_count']
            text = tweet['text'].lower().strip(".")
            retweet_count_map[text]=retweet_count
            tweet_length= len(text)
            tweets.append(text)
            followers= tweet['user']['followers_count']
            if is_primetime(parser.parse(tweet['created_at'])):
                primetime_tweets+=1
            else:
                nonprimetime_tweets+=1
    most_retweeted=sorted(retweet_count_map, key=lambda x:retweet_count_map[x], reverse=True)
    if len(most_retweeted)>5:
        most_retweeted=most_retweeted[:5]
    session["followers"]=followers
    session["picture_url"]= picture_url
    session["name"]= verify['name']
    session["primetime_tweets"]=primetime_tweets
    session["nonprimetime_tweets"]=nonprimetime_tweets
    User.get_or_create(verify['screen_name'], verify['id'])
    session['tweets']=retweet_count_map
    session['word_tfidf']= get_tfidf_of_words(retweet_count_map)
    session['tweet_length']= get_retweets_based_on_tweet_length(retweet_count_map)
    session['most_retweeted']=most_retweeted

    return redirect(url_for('profile'))


@app.route('/twitter/profile')
def profile():
    highest_scoring_words=sorted(session["word_tfidf"], key=lambda x:session["word_tfidf"][x], reverse=True)[:5]
    tfidf_scores=[]
    for word in highest_scoring_words:
        tfidf_scores.append(session["word_tfidf"][word][0])
    return render_template('profile.html', followers= session["followers"], name=session["name"], \
                        primetime_tweets=session["primetime_tweets"], nonprimetime_tweets=session["nonprimetime_tweets"],\
                        picture=session["picture_url"], tfidf_scores=tfidf_scores, highest_scoring_words=highest_scoring_words,\
                        tweet_length= session["tweet_length"], most_retweeted=session["most_retweeted"])


def get_tfidf_of_words(retweet_count_map):
    word_tfidf={}
    s=open('english').read()
    for tweet, retweet_count in retweet_count_map.iteritems():
        for word in filter(lambda w: not w in s,tweet.split()):
            if not word in word_tfidf:
                word_tfidf[word]=[]
            word_tfidf[word].append(retweet_count)
    for tweet, retweet_list in word_tfidf.iteritems():
        word_tfidf[word]=int(numpy.mean(retweet_list))
    return word_tfidf

def get_retweets_based_on_tweet_length(retweet_count_map):
    retweets_based_on_tweet_length=[]
    for tweet, retweet_count in retweet_count_map.iteritems():
        lst=[]
        lst.append(len(tweet))
        lst.append(retweet_count)
        retweets_based_on_tweet_length.append(lst)
    return retweets_based_on_tweet_length


def is_primetime(date):
    return date.hour > 16 and date.hour < 22
  

if __name__ == '__main__':
    db.create_all()
    app.run()