from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, Text

engine = create_engine('sqlite:///twitlab.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()

session = Session()

class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    tid = Column(String(21))
    favorite_count =  Column(Integer)
    retweet_count = Column(Integer)
    text = Column(Text)
    created_at = Column(DateTime)

Base.metadata.create_all(engine) 