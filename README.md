# Description 

A social media marketing tool that uses machine learning to predict the user engagement of a tweet

# Installation

    pip install -r requirements.txt

# Data

Data we collected (in the form of full postgres database dump) can be found at https://s3.amazonaws.com/twitlab/twitlab.gz
    
# Setup

## database.py

This file defines the schema definitions and connects to the database using the SQLAlchemy framework. It imports settings from the settings.py or local_settings.py files depending on the environment

## local_settings.py/settings.py

These files contain the settings for connecting to the local and production databases respectively. The format is:

    DATABASE = {
                    'drivername': <db_driver>,
                    'host': <host>,
                    'port': <port>,
                    'username': <username>,
                    'password': <password>,
                    'database': <db>
                }

## keys.py


To scrape data using twitterstream.py, create a keys.py file with the following key values that you obtain from twitter:


    ckey = consumerKeyHere
    csecret = consumerSecretHere
    atoken = accessTokenHere
    asecret = accessSecretHere

## twitterstream.py

Scrapes Twitter's POST /statuses/filter endpoint and counts retweets using the credentials in keys.py, with the popular words defined in popwords.txt, and stores them using the Tweet schema into the database. Also, inserts users from each tweet into the user table.

## twitterstatus.py

Iterates over all tweets in the tweets table in batches of 100 and hits Twitter's GET /statuses/lookup endpoint while handling the rate limit and window. Inserts tweets from the tweets table into the processed_tweets table using the ProcessedTweet schema.

## popword.txt

List of top 500 words used in a sample of tweets taken from http://techland.time.com/2009/06/08/the-500-most-frequently-used-words-on-twitter/

## word_tfidf.py

Calulates the TF-IDF score for 200,000 processed tweets whose result is contained in highest_tfidf_words.txt.

## regression.py

Calculates a linear regression model using the length of a tweet in characters, the number of retweets it has, and whether or not it was during prime time or not.

# Other

## tweet_tfidf.py

An incomplete, not working script that intends to calculate the TF-IDF score of each processed tweet.

## historics_api.py

Our initial attempts to use Datasift as our data source before realizing it was not feasible.

## manage.py

For running the app

## Procfile

Deployment file for Heroku