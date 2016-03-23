# -*- coding: utf-8 -*-

import sys
import Queue
import threading
import logging
import math
from ..models import Ad



class Controller( threading.Thread ):
  """Threaded Url Grab"""

  def __init__( self, engine, session ):
    threading.Thread.__init__(self)

    self.queue = Queue.Queue()
    self.engine = engine
    self.session = session


  def run( self ):
    engine = self.engine
    session = self.session
    while True:
      
      search = self.queue.get()
      logging.debug( '%s controller get %s search request' % (self.engine.name, search.name) )
      
      for preview in engine.search( search.query ):
        orm_ad = session.query(Ad).filter( Ad.url == preview.url ).first()

        if not orm_ad:
          orm_ad = Ad(url=ad.url)

        for k,v in ad.items():
          setattr(orm_ad, k ,v)

        session.add(orm_ad)
        session.flush()
        session.commit()
