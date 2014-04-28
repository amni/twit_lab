
print "earliest possible test"
from tweepy import API
from tweepy import OAuthHandler
from tweepy.binder import bind_api
from tweepy.utils import list_to_csv
from keys import *
import sys
print "pretest"

import database as db
Tweet = db.Tweet
User= db.User
session = db.session

def lookup_statuses(self, status_ids=None):
        return self._lookup_statuses(list_to_csv(status_ids))

_lookup_statuses = bind_api(
    path = '/statuses/lookup.json',
    payload_type = 'status', payload_list = True,
    allowed_param = ['id'],
)

API.lookup_statuses = lookup_statuses
API._lookup_statuses = _lookup_statuses

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = API(auth)

tweets = session.query(Tweet).limit(100)

ids = list()

for tweet in tweets:
	ids.append(int(tweet.tid))

statuses = api.lookup_statuses(ids)

for status in statuses:
	print(dir(status))
	break

# for tweet in tweets:
# 	print(tweet.tid)
# 	if tweet.tid:
# 		# try:
# 		status = api.get_status(int(tweet.tid))
# 		print status
# 		break
# 		user=User.query.filter_by(id=status.user_id).first()
# 		print ("User followers: %d" % user.followers_count)
			
		# except:
		# 	print "Unexpected error:", sys.exc_info()[0]
		# 	break
		# print ("Retweets: %d" % status.retweet_count)
		# print

# print(dir(status))
# print(status.retweet_count)
