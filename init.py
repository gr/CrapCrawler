#!./venv/bin/python
# -*- coding: utf-8 -*-
 
import sys 
import argparse 
import traceback
import os
import yaml
from crawler.crawlerdaemon import CrawlerDaemon
from crawler.common import AttrDict
import logging, logging.config
import threading

 
def installThreadExcepthook():
    """
    Workaround for sys.excepthook thread bug
    From
http://spyced.blogspot.com/2007/06/workaround-for-sysexcepthook-bug.html
   
(https://sourceforge.net/tracker/?func=detail&atid=105470&aid=1230540&group_id=5470).
    Call once from __main__ before creating any threads.
    If using psyco, call psyco.cannotcompile(threading.Thread.run)
    since this replaces a new-style class method.
    """
    init_old = threading.Thread.__init__
    def init(self, *args, **kwargs):
        init_old(self, *args, **kwargs)
        run_old = self.run
        def run_with_except_hook(*args, **kw):
            try:
                run_old(*args, **kw)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                sys.excepthook(*sys.exc_info())
        self.run = run_with_except_hook
    threading.Thread.__init__ = init

 
if __name__ == "__main__":
  cwd = os.path.dirname(os.path.abspath(__file__))


  parser = argparse.ArgumentParser(description='Crap crawler' )
  parser.add_argument('action', choices=['start', 'stop', 'status', 'restart'], 
                                    help='Action to init service')
  parser.add_argument('--pid' , default=cwd + '/run/getIt.pid',
                                          help='Path to pid file')
  parser.add_argument('--host', default="0.0.0.0", type=str, 
                                help='eth interface')
  parser.add_argument('--port', default=8080, type=int, 
                                help='Tcp port for web interface')
  parser.add_argument('--database', default=cwd + '/run/db/crawler.sqlite3', 
                                  help='Path to sqlite3 database')
  parser.add_argument('--crawler-ua', default='Crap Crawler', 
                                    help='User-Agent for crawler')
  parser.add_argument('--config', default=cwd + '/etc/default.yaml', 
                                       help='Path to config file')
  parser.add_argument('--dry-run', default=True, 
                                       help='Path to config file')
  parser.add_argument('--logconfig', default=cwd + '/etc/logger.cfg', 
                                       help='Path to log config file')
  args = parser.parse_args()

  logging.config.fileConfig( args.logconfig ) 
  logging.debug('Read logconfig %s' % args.logconfig )
  # write all exceptions to log via logger module
  def logger_handler(type, value, tb):
      logging.exception("Uncaught exception: %s\n%s" % ( value, '\n'.join( traceback.format_tb(tb) )  ) )
  # Install exception handler
  sys.excepthook = logger_handler
  installThreadExcepthook()


  # Read config
  with file( args.config ) as f:
    config = AttrDict( yaml.load(f.read()) )
    logging.debug('Read config %s' % args.config )

  # override arguments from cli
  for k, v in args.__dict__.items():  
    config[k] = v
    logging.debug('Config setting was overridden by CLI argument %s = %s' % (k,v) )

  # Initialize Crawler Daemon
  daemon = CrawlerDaemon( args.pid  )
  daemon.config = config

  if 'start' == args.action:
    daemon.start()
  elif 'stop' == args.action:
    daemon.stop()
  elif 'restart' == args.action:
    daemon.restart()
  elif 'status' == args.action:
    daemon.status()

