# -*- coding: utf-8 -*-

import logging
import schedule
import time
from daemon import Daemon
from models import Engine as ORM_Engine
from models import Search
from models import get_session
from crawler.engine import Engine
from crawler.controller import Controller 
from web import httpd


class CrawlerDaemon(Daemon):
  config = None
  controllers = dict()

  def run(self):
    logging.info('CrawlerDaemon run')
    sqlite_session = get_session( self.config.database )
    orm_engines = sqlite_session.query( ORM_Engine ).all()

    if not self.config.dry_run:
      if len( orm_engines ) == 0:
        logging.debug( 'Crawler has no engines' )
         
      # Start controllers in each thread 
      for orm_engine in orm_engines:
        logging.info('Load orm_engine: %s' % orm_engine.name )
        engine = Engine( orm_engine )
        self.controllers[ engine.name ] = Controller( engine, sqlite_session ) 
        self.controllers[ engine.name ].start()
      
      # Start scheduling searches 
      for orm_search in sqlite_session.query( Search ).all():
        for engine in orm_search.engines:
          job = lambda: self.controllers[ engine.name ].queue.put( orm_search )
          schedule.every( orm_search.periodicity ).seconds.do( job )
          logging.debug('Put %s to schedule with periodicity %i seconds' % ( orm_search.name, orm_search.periodicity ) )

    self.httpd = httpd( self.config, self.controllers )
     
    while True:
      if not self.config.dry_run:
        schedule.run_pending()

      self.httpd._handle_request_noblock()
      time.sleep(1)

   
  def status(self):
    logging.info('CrawlerDaemon status')
    #TODO pass some info
    print "Don't know status"

  def stop(self):
    logging.info('CrawlerDaemon stop')
    #TODO graceful stop
    super(CrawlerDaemon, self).stop()


  def start(self):
    logging.info('CrawlerDaemon start')
    super(CrawlerDaemon, self).start()

