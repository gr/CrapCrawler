# -*- coding: utf-8 -*-
import logging;logging.basicConfig(level = logging.DEBUG)
import os

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, create_engine
from sqlalchemy import ForeignKey, Table, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

# association tables
search_engine = Table('search_engine', Base.metadata,
    Column('search_id', Integer, ForeignKey('searches.id')),
    Column('engine_id', Integer, ForeignKey('engines.id'))
)

manager_contact = Table('manager_contact', Base.metadata,
    Column('manager_id', Integer, ForeignKey('managers.id')),
    Column('contact_id', Integer, ForeignKey('contacts.id'))
)

search_managers = Table('search_managers', Base.metadata,
    Column('search_id', Integer, ForeignKey('searches.id')),
    Column('manager_id', Integer, ForeignKey('managers.id'))
)


# ORM models
class Field(Base):
  __tablename__ = 'fields'

  def __init__(self, type=None, purpose=None, name=None, xpath=None, engine=None):
    self.type    = type
    self.purpose = purpose
    self.name    = name   
    self.xpath   = xpath  
    self.engine  = engine 


  id      = Column(Integer, primary_key=True)
  type    = Column(Enum('int', 'str', 'url', 'price', 'date', 'image', name='field_types')) 
  purpose = Column(Enum('preview', 'ad', 'search', name='field_purpose'))
  name    = Column(String(50))
  xpath   = Column(String(350))
  engine  = Column(Integer, ForeignKey('engines.id')) 
  
  def __repr__(self):
    return "<Field (id=%i, name=%s, engine=%s)>" % (self.id, self.name, self.engine.name)


class Engine(Base):
  __tablename__ = 'engines'

  id       = Column(Integer, primary_key=True)
  name     = Column(String(50))
  url      = Column(String(350))
  encoding = Column(String(50))
  delay    = Column(Integer)
  eop      = Column(String(350))
  fields   = relationship("Field")
  preview_price = Column(Boolean, default=False)

  def __repr__(self):
    return "<Engine (id=%i, name=%s)>" % (self.id, self.name)


class Ad(Base):
  __tablename__ = 'ads'

  id    = Column(Integer, primary_key=True)
  url   = Column(String(350))
  title = Column(String(350))
  price = Column(Integer)

  def __repr__(self):
    return "<Ad (id=%i, name=%s)>" % (self.id, self.name)


class Search(Base):
  __tablename__ = 'searches'

  id          = Column(Integer, primary_key=True)
  name        = Column(String(50))
  query       = Column(String(350))
  min_price   = Column(Integer)
  max_price   = Column(Integer)
  periodicity = Column(Integer)
  enabled     = Column(Boolean, default=False)
  engines     = relationship('Engine', secondary=search_engine, backref='searches')
  manager     = relationship('Manager', secondary=search_managers, backref='searches')
  notice_by   = Column(Enum('email', 'phone', 'push', name='contact_types'))

  def __repr__(self):
    return "<Search (id=%i, name=%s)>" % (self.id, self.name)


class Manager(Base):
  __tablename__ = 'managers'

  id       = Column(Integer, primary_key=True)
  name     = Column(String(50))
  contacts = relationship('Contact', secondary=manager_contact, backref='managers')

  def __repr__(self):
    return "<Manager (id=%i, name=%s)>" % (self.id, self.name)


class Contact(Base):
  __tablename__ = 'contacts'

  def __init__(self, type=None, contact=None):
    self.type    = type
    self.contact = contact
    
  id      = Column(Integer, primary_key=True)
  type    = Column(Enum('email', 'phone', 'push', name='contact_types'))
  contact = Column(String(50))

  def __repr__(self):
    return "<Contact (id=%i, name=%s)>" % (self.id, self.name)


