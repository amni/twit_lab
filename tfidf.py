# -*- coding: utf-8 -*-
import nltk
import json
import string
import operator
import nltk.corpus
from keys import *
from time import sleep
from tweepy import API
from tweepy import OAuthHandler
from collections import Counter
from nltk.corpus import stopwords

from guess_language import guess_language

import database as db

word_RTcount_list = []
word_Tcount_list = []
word_tfidf_list = []

word_RTcount_dict = {}
word_Tcount_dict = {}
word_tfidf_dict = {}

def fetch_word():

	Tweet = db.Tweet
	session = db.session

	tweets = session.query(Tweet).all()
	all_words = ''

	for tweet in tweets:
		if tweet.text:
			if guess_language(tweet.text) == 'en':
				tweet_text = str(tweet.text.encode('utf-8'))
				tweet_lower = tweet_text.lower()
				tweet_final = tweet_lower.translate(None, string.punctuation)
			
			# Concatenate all words (including hashtags) in tweet
				all_words = all_words + ' ' + tweet_final

	return all_words


def tokenize(all_words):

    tokens = nltk.word_tokenize(all_words)
    return tokens

# Eradicate stop words calculate TFIDF values below:

words = fetch_word()
tokens = tokenize(words)
all_words = [w for w in tokens if not w in stopwords.words('english')]

# Query for RT values 

Tweet = db.Tweet
session = db.session

tweets = session.query(Tweet).all()

for tweet in tweets:

	if guess_language(tweet.text) == 'en':
		tweet_text = str(tweet.text.encode('utf-8'))

		# Find unique words (including hashtags) per tweet
		tweet_lower = tweet_text.lower()
		tweet_final = tweet_lower.translate(None, string.punctuation)
		unique_word_list = nltk.word_tokenize(tweet_final)

		# Calculate total RTs and Tweets to find TFIDF
		for word_in_tweet in unique_word_list:
			if word_in_tweet in all_words:

				if word_in_tweet in word_RTcount_dict:
					if word_RTcount_dict[word_in_tweet] != None:
						word_RTcount_dict[word_in_tweet] = word_RTcount_dict[word_in_tweet] + tweet.retweet_count
						#print 'word_RTcount_dict[word_in_tweet]' + str(word_RTcount_dict[word_in_tweet])
				else:
					word_RTcount_dict[word_in_tweet] = tweet.retweet_count
					#print 'word_RTcount_dict[word_in_tweet]' + str(word_RTcount_dict[word_in_tweet])

				if word_in_tweet in word_Tcount_dict:
					if word_Tcount_dict[word_in_tweet] != None:
						word_Tcount_dict[word_in_tweet] = word_Tcount_dict[word_in_tweet] + 1
						#print 'word_Tcount_dict[word_in_tweet]' + ' ' +  word_in_tweet + ' ' + str(word_Tcount_dict[word_in_tweet])
				else:
					word_Tcount_dict[word_in_tweet] = 1
					#print 'word_Tcount_dict[word_in_tweet]' + ' ' +  word_in_tweet + ' ' + str(word_Tcount_dict[word_in_tweet])


tfidf_dict = {}

for word in word_Tcount_dict:
	num_RT = None
	num_Tweet = None
	key = ''

	for entry in word_RTcount_dict:
		#print "Key: " + str(entry)
		#print "Retweets: " + str(word_RTcount_dict[entry])
		num_RT = word_RTcount_dict[entry]

	for entry in word_Tcount_dict:
		#print "Key: " + str(entry)
		#print "Tweet Count: " + str(word_Tcount_dict[entry])
		num_Tweet = word_Tcount_dict[entry]

	tfidf_value = num_RT/num_Tweet

	tfidf_dict[word] = tfidf_value

tfidf_sorted = sorted(tfidf_dict.iteritems(), key=operator.itemgetter(1))

print 'Word retweet popularity in descending order:'
for x in tfidf_sorted:
	print x






