from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean, ForeignKey, BigInteger

from sqlalchemy.engine.url import URL

import settings


engine = create_engine('sqlite:///twitlab2.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()

session = Session()

class ProcessedTweet(Base):
	__tablename__='processedtweets'
	id = Column(Integer, primary_key=True)
	retweet_count = Column(Integer)
	text = Column(Text)
	primetimetweet = Column(Integer)
	num_followers= Column(Integer)





Base.metadata.create_all(engine) 