import nltk
import string
import nltk.corpus

from collections import Counter
from nltk.corpus import stopwords

class tfidf_test:

	def parse():
		file = open('sample_data.json','r')
		all_words = ''

		# Parses tweet so tweet only containts relevant text.
		for tweets in file:
			# Fetch Tweet
			tweet = tweets.split()

			# Gets rid of '"text:"'
			tweet = tweet[1:len(tweet)]

			# Convert to String
			tweet_string = " ".join(tweet);

			# Filter only relevant text
			# Tweet text arbitrarily ends either on '"created_at":'' or '"id":''
			# IDKl Why
			createAt_index = tweet_string.find('"created_at":')
			id_index = tweet_string.find('"id":')

			end_index = 0
			if createAt_index == -1:
				end_index = id_index
			else:
				end_index = createAt_index

			tweet_text = tweet_string[0:end_index]
			tweet_lower = tweet_text.lower()
			tweet_final = tweet_lower.translate(None, string.punctuation)
			
			# Concatenate all tweets
			all_words = all_words + ' ' + tweet_final

		return all_words


	def tokenize(words):

	    tokens = nltk.word_tokenize(words)
	    return tokens


	words = parse()	
	tokens = tokenize(words)
	filtered = [w for w in tokens if not w in stopwords.words('english')]
	count = Counter(filtered)
	print type(filtered)
	# print count.most_common(100) 

