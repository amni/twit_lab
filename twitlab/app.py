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

    params = {'include_rts': 1,  # Include retweets
          'count': 100000}       # 10 tweets

    r = sess.get('statuses/user_timeline.json', params=params)

    messages={}
    tweets=[]
    for i, tweet in enumerate(r.json(), 1):
        if not "retweeted_status" in tweet: 
            retweet_count= tweet['retweet_count']
            text = tweet['text']
            tweets.append(text)
            print text
            print retweet_count

    messages["tweets"]= tweets

    User.get_or_create(verify['screen_name'], verify['id'])
    session['messages']=messages
    flash('Logged in as ' + verify['name'])
    return redirect(url_for('profile'))


@app.route('/twitter/profile')
def profile():
    print session["messages"]  
    return render_template('profile.html')


if __name__ == '__main__':
    db.create_all()
    app.run()