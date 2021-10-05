from sqlalchemy import Table, Column, Integer, String, DateTime, \
    MetaData, ForeignKey, select, create_engine, \
    PrimaryKeyConstraint, UniqueConstraint, \
    ForeignKeyConstraint, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from datetime import datetime

ENGINE = create_engine('sqlite:///./memegarbage.db')
SESSION = Session(bind=ENGINE)
BASE = declarative_base(bind=ENGINE)


class Upload(BASE):
    __tablename__ = 'uploads'
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("downloads.document_id"))
    uploaded_on = Column(DateTime, default=datetime.now)
    downloaded_on = relationship("Download")


class Download(BASE):
    __tablename__ = 'downloads'
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String, ForeignKey("videos.document_id"))
    group = Column(String, ForeignKey("groups.name"))


class Video(BASE):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, nullable=False, unique=True)
    group = Column(String, ForeignKey("groups.name"))
    created_on = Column(DateTime, default=datetime.now)
    already_used = Column(Boolean, default=False)

class Group(BASE):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    created_on = Column(DateTime, default=datetime.now)


BASE.metadata.create_all(ENGINE)
