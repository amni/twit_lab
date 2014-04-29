from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean, ForeignKey, BigInteger

from sqlalchemy.engine.url import URL

import local_settings

# DB Setup
engine = create_engine(URL(**local_settings.DATABASE))
Session = sessionmaker(bind=engine)

Base = declarative_base()

session = Session()

# User Object Schema
class User(Base):
	__tablename__ = 'user'

	id= Column(BigInteger, primary_key=True)
	created_at=Column(DateTime)
	default_profile= Column(Boolean)
	default_profile_img= Column(Boolean)
	followers_count= Column(Integer)
	friends_count=Column(Integer)
	user_name= Column(String(50))
	location = Column (String(200))
	statuses_count= Column(Integer)

# Tweet Object Schema
class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    tid = Column(String(21))
    favorite_count =  Column(Integer)
    retweet_count = Column(Integer)
    text = Column(Text)
    created_at = Column(DateTime)
    user_id = Column(BigInteger, ForeignKey('user.id'))

# Processed Tweet Object Schema
class ProcessedTweet(Base):
    __tablename__='processed_tweets'
    id = Column(Integer, primary_key=True)
    tid = Column(String(21))
    retweet_count = Column(Integer)
    text = Column(Text)
    primetimetweet = Column(Integer)
    num_followers= Column(Integer)
    tfidf= Column(Integer)

Base.metadata.create_all(engine) 