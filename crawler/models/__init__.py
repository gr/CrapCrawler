# -*- coding: utf-8 -*-

from models import Field, Engine, Ad, Search, Manager, Contact, Base

import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import  create_engine


# This function return SQLAlchemy session 
def get_session( db_path, logging_flag=False, checkfirst=True ):
  logging.debug( 'Create database session: %s ' % db_path )

  database_engine = create_engine( 'sqlite:///%s' % db_path,
                                   connect_args={'check_same_thread':False},
                                   echo=logging_flag )
  Base.metadata.create_all( bind=database_engine, checkfirst=checkfirst )

  Session = sessionmaker( bind=database_engine )
  return Session()

