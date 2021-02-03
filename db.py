from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from scrapers import Talk
import pickle
from scrapers import pickleLoader

Base = declarative_base()


class DBTalk(Base):
    __tablename__ = 'talk'

    # id = Column("rowid", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String, nullable=True)

    abstract = Column("abstract", String, nullable=True)

    link = Column("link", String, nullable=False, primary_key=True)
    speaker_name = Column("speaker_name", String, nullable=True)

    speaker_id = Column(
        "speaker_id",
        Integer,
        ForeignKey("speaker.id"),
        nullable=True)
    workshop_id = Column(
        "workshop_id",
        Integer,
        ForeignKey("workshop.id"),
        nullable=True)


class DBSpeaker(Base):
    __tablename__ = 'speaker'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    last_name = Column("last_name", String, nullable=False)

    UniqueConstraint('name', name='speaker_name')


class DBWorkshop(Base):
    __tablename__ = 'workshop'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String, nullable=False)
    UniqueConstraint('title', name='unique_title')


def prepareSession(sqlfile='videoarxiv.sqlite3'):
    engine = create_engine('sqlite:///' + sqlfile)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def addTalk(talk: Talk, session):

    try:
        if newTalk := session.query(DBTalk).filter_by(link=talk.link).first():
            return newTalk
    except BaseException:
        pass

    speaker = addSpeaker(talk.firstName, talk.lastName, session)
    speaker_name = None
    speaker_id = None
    if speaker is not None:
        speaker_name = speaker.name
        speaker_id = speaker.id
    workshop = addWorkshop(talk.workshop, session)
    workshop_id = None
    if workshop is not None:
        workshop_id = workshop.id
    newTalk = DBTalk(
        title=talk.title,
        abstract=talk.abstract,
        link=talk.link,
        speaker_name=speaker_name,
        speaker_id=speaker_id,
        workshop_id=workshop_id)

    session.add(newTalk)
    session.commit()
    return newTalk


def addSpeaker(firstName, lastName, session) -> Union[DBSpeaker, None]:
    fullName = ""
    if firstName:
        fullName = firstName + ' '
    if lastName:
        fullName = fullName + lastName
    else:
        return None
    try:
        if newSpeaker := session.query(
                DBSpeaker).filter_by(name=fullName).first():
            return newSpeaker
    except BaseException:
        pass

    newSpeaker = DBSpeaker(name=fullName, last_name=lastName)
    session.add(newSpeaker)
    session.commit()
    return newSpeaker


def addWorkshop(workshop, session) -> Union[DBWorkshop, None]:
    if not workshop:
        return None
    else:
        try:
            if newWorkshop := session.query(
                    DBWorkshop).filter_by(title=workshop).first():
                return newWorkshop
        except BaseException:
            pass

        newWorkshop = DBWorkshop(title=workshop)
        session.add(newWorkshop)
        session.commit()
        return newWorkshop


# infileNames = [
    # 'talks_msri_reversed.p']
# # 'talks_birs.p',
# # 'talks_fields.p',
# # 'talks_simons.p',
# # 'talks_ihes.p',
# # 'talks_ias.p',
# # 'talks_mathtube.p']
# for infileName in infileNames:
    # print(infileName)
    # with open(infileName, "rb") as infile:
        # for talk in pickleLoader(infile):
        # addTalk(talk)
