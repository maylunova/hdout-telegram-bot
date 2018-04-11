from sqlalchemy import create_engine, Column, Integer, Text, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///hdout.db')
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer())
    hdout_id = Column(Integer())

    def __repr__(self):
        return '<User ID {} {} {}>'.format(self.id, self.chat_id, self.hdout_id)


class SentMessage(Base):
    __tablename__ = 'Sent_Messages'
    id = Column(Integer, primary_key=True)
    episode_name = Column(Text())
    user_id = Column(Integer(), ForeignKey('Users.id'))

    def __repr__(self):
        return '<{} {}>'.format(self.user_id, self.episode_name)


def add_user_to_db(chat_id, hdout_id):
    user = User.query.filter(User.chat_id == chat_id, User.hdout_id == hdout_id).first()
    if user is None:
        user = User(chat_id=chat_id, hdout_id=hdout_id)
        db_session.add(user)
    db_session.commit()
    return user.id


def add_epi_to_db(title, user_id):
    pair = SentMessage.query.filter(SentMessage.episode_name == title, SentMessage.user_id == user_id).first()
    if pair is None:
        pair = SentMessage(episode_name=title, user_id=user_id)
        db_session.add(pair)
    db_session.commit()


def check_db(user_id, title):
    pair = SentMessage.query.filter(SentMessage.episode_name == title, SentMessage.user_id == user_id).first()
    if pair is None:
        return False


def create_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_db()

