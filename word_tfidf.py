import database as db
import numpy
import operator

ProcessedTweet = db.ProcessedTweet
session = db.session

tweets = session.query(ProcessedTweet).limit(200000)

word_retweets={}
word_tfidf={}

for tweet in tweets:
	for word in tweet.text.split():
		word=word.lower().strip(".")
		if word not in word_retweets:
			word_retweets[word]=[]
		word_retweets[word].append(tweet.retweet_count)

for tweet, retweet_list in word_retweets.iteritems():
	if len(retweet_list)>2:
		word_tfidf[tweet]= numpy.mean(retweet_list)



print sorted(word_tfidf.iteritems(), key=operator.itemgetter(1))

