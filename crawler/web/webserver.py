# -*- coding: utf-8 -*-
 
import BaseHTTPServer
import logging
import json
import os
import sys
from ..models import Field, Engine, Ad, Search, Manager, Contact, Base, get_session
from sqlalchemy.orm import class_mapper
import threading



avaliable_types = ('engine', 'field', 'search', 'ad',  'manager')

def serialize(model):
  """Transforms a model into a dictionary which can be dumped to JSON."""
  # first we get the names of all the columns on your model
  columns = [c.key for c in class_mapper(model.__class__).columns]
  # then we return their values in a dict
  return dict((c, getattr(model, c)) for c in columns)


class CrawlerWeb(BaseHTTPServer.BaseHTTPRequestHandler):

  def do_HEAD(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()


  def do_POST(self):
    self.do_UNIVERSAL()


  def do_GET(self):
    self.do_UNIVERSAL()


  def do_UNIVERSAL(self):
    method = self.path.split('?')[0][1:].replace('/', '_') # remove args and first /, replace / with _
    if method in ('', 'index.html', 'index_', 'index__'):
      method = 'index'

    if method.startswith('do_') or not hasattr(self, method) or not callable(getattr(self, method)):
      self.do_404()
    else:
      getattr(self, method)()


  def do_404(self):
    self.send_response(404)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    self.wfile.write('No such file or directory <br> <p>%s</p>' % self.path)

    
  def do_200(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    

  def index(self):
    self.path = '/static?index.html'
    self.static()


  def static(self):
    cwd = os.path.dirname(os.path.abspath(__file__))
    www_root = '/../../share/www/'
    filename = self.path.split('?')[1].replace('..', '.')

    filename = cwd + www_root + filename
    
    if not os.path.isfile( filename ):
      self.do_404()
    else:
      self.do_200()
      for line in file( filename,'r'):
        self.wfile.write( line )

    
  def list(self):
    list_type = self.path.split('?')[1][:-1]
    if list_type in avaliable_types:
      sqlite_session = get_session( self.config.database )
      items = sqlite_session.query( eval(list_type.capitalize()) ).all()

      self.do_200()
      response = dict()
      response['headers'] = [ c.key for c in class_mapper(items[0].__class__).columns ] 
      response['data'] = [ [ getattr(item, k) for k in response['headers'] ] for item in items ]
      self.wfile.write( json.dumps(response) )
    else:
      self.do_404()


class HTTPD( threading.Thread ):
  """ Threaded http server """

  def __init__( self, config, controllers ):
    threading.Thread.__init__(self)
    
    self.config = config
    self.controllers = controllers
    self.httpd = BaseHTTPServer.HTTPServer( (self.config.host, self.config.port), CrawlerWeb ) 
  
  def run( self ):
    logging.info('Webserver starting %s:%s' % ( self.config.host, self.config.port ))
    self.httpd.serve_forever()
   

