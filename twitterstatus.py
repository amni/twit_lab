
print "earliest possible test"
from tweepy import API
from tweepy import OAuthHandler
from tweepy.binder import bind_api
from tweepy.utils import list_to_csv
from tweepy.error import TweepError
from keys import *
import time, math
print "pretest"

# Create DB instances
import database as db
Tweet = db.Tweet
User= db.User
ProcessedTweet = db.ProcessedTweet
session = db.session

# Add API methods
def lookup_statuses(self, status_ids=None):
        return self._lookup_statuses(list_to_csv(status_ids))

_lookup_statuses = bind_api(
    path = '/statuses/lookup.json',
    payload_type = 'status', payload_list = True,
    allowed_param = ['id'],
)

API.lookup_statuses = lookup_statuses
API._lookup_statuses = _lookup_statuses


# Init API
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = API(auth)

# Primtime calculation helper
def calc_primetime(date):
	if date.hour > 16 and date.hour < 22:
		return 1
	else:
		return 0

# Set constants
total_count = session.query(Tweet).count()
current_limit = 100
window_time = 900

# Set initial variables
current_offset = 0
window_beginning = math.floor(time.time())

stat_file = open('stat.txt', 'w')

while current_offset < total_count:
	tweets = session.query(Tweet).offset(current_offset).limit(current_limit)
	ids = list()
	for tweet in tweets:
		ids.append(tweet.tid)
	try:
		statuses = api.lookup_statuses(ids)
	except TweepError:
		window_end = math.ceil(time.time())
		time.sleep(window_time - (window_end - window_beginning) + 10)
		window_beginning = math.floor(time.time())
		statuses = api.lookup_statuses(ids)

	for status in statuses:
		is_primetime = calc_primetime(status.created_at)
		ptweet = ProcessedTweet(tid=status.id, retweet_count=status.retweet_count, text=status.text,
			primetimetweet=is_primetime, num_followers=status.user.followers_count)
		session.add(ptweet)
	session.commit()
	stat_file.write(str(current_offset)+'\n')
	current_offset += current_limit
