from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean, ForeignKey, BigInteger

from sqlalchemy.engine.url import URL

import settings


engine = create_engine(URL(**settings.DATABASE))
Session = sessionmaker(bind=engine)

Base = declarative_base()

session = Session()

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

class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    tid = Column(String(21))
    favorite_count =  Column(Integer)
    retweet_count = Column(Integer)
    text = Column(Text)
    created_at = Column(DateTime)
    user_id = Column(BigInteger, ForeignKey('user.id'))



Base.metadata.create_all(engine) 