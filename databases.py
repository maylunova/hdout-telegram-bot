from sqlalchemy import create_engine, Column, Integer, Text, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///hdout.db')
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Users(Base):
    __tablename__ = 'Users'
    hdout_id = Column(Integer(), primary_key=True)
    messages = relationship('SentMessages', backref='Users')
    # tlgrm_id = Column(Integer())
    # username = Column(Text())

    def __repr__(self):
        return '<User ID {}>'.format(self.hdout_id)


class SentMessages(Base):
    __tablename__ = 'Sent_Messages'
    hdout_id = Column(Integer(), ForeignKey('Users.hdout_id'), primary_key=True)
    episodes = Column(Text(), primary_key=True)

    def __repr__(self):
        return '<{} {}>'.format(self.hdout_id, self.episodes)


def add_to_db(hdout_id, title):
    user = Users.query.get(hdout_id)
    if user is None:
        user = Users(hdout_id=hdout_id)
        db_session.add(user)
    pair = SentMessages.query.get((hdout_id, title))
    if pair is None:
        pair = SentMessages(hdout_id=hdout_id,
                            episodes=title)
        db_session.add(pair)
    db_session.commit()


def check_db(hdout_id, title):
    pair = SentMessages.query.get((hdout_id, title))
    if pair is None:
        return False


def create_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_db()

