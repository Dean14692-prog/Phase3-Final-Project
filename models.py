from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    tell = Column(Integer)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now())

    notes = relationship('Note', back_populates='user')
    complaints = relationship('Complaint', back_populates='user')

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime)

    user = relationship('User', back_populates='notes')
    tags = relationship('Tag', secondary='note_tags', back_populates='notes')

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key = True, autoincrement = True)
    tag_name = Column(String)
    notes = relationship('Note', secondary='note_tags', back_populates='tags')


class NoteTag(Base):
    __tablename__ = 'note_tags'
    note_id = Column(Integer, ForeignKey('notes.id'), primary_key= True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

class Complaint(Base):
    __tablename__ = 'complaint'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text)
    status = Column(String)
    created_at = Column(DateTime)
    user = relationship('User', back_populates='complaints')



