#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import requests
import time
from lxml import etree
from lxml.html import fromstring, tostring
from ..common import AttrDict
from datetime import datetime as dt, timedelta as td, date
from field_types import FieldTypes


class Engine(object):
  
  field_types = FieldTypes()
  
  def __init__(self, orm_engine):
    self.name = orm_engine.name
    self.url = orm_engine.url
    self.delay = orm_engine.delay
    self.eop = orm_engine.eop
    self.preview_price = orm_engine.preview_price
    self.preview_fields = filter( lambda x: x.purpose == 'preview', orm_engine.fields)
    self.ad_fields = filter( lambda x: x.purpose == 'ad', orm_engine.fields)
    self.ads_xpath = filter( lambda x: x.purpose == 'search', orm_engine.fields)[0]
    self.encoding = orm_engine.encoding
    self.max_search_pages = 20
    self.recieved_bytes = 0
    self.performed_searches = 0
    self.no_ads_on_page = 0
    
    logging.info('Initialize %s driver' % self.name.capitalize() )
    logging.info('Search url pattern: %s' % self.url )


  def get_page(self, url):
    logging.debug( 'Wait engine page load timeout %i sec' % self.delay )
    time.sleep( self.delay )
    logging.info( 'Download follow url: %s' % str(url) )
    r = requests.get( url )
    logging.info( 'Response code: %i; %i bytes' % (r.status_code, len(r.content)) )
    self.recieved_bytes += len(r.content)
    return ( r.status_code, r.content.decode( self.encoding ) )


  def search(self, query):
    self.performed_searches += 1
    for x in xrange(1, self.max_search_pages):
      url = self.url.replace('<query>', query).replace('<pagination>', str(x))
      ( return_code, content ) = self.get_page( url )

      if return_code != 200:
        logging.info( 'Response code: %i; stop paginating' % return_code )
        break

      tree = fromstring( content )
      ads = tree.xpath( self.ads_xpath.xpath )

      if len(ads) == 0:
        logging.warning( 'Find no ads on %s page! Recheck ads field of %s engine' % (url, self.name) )
        self.no_ads_on_page += 1
        break

      logging.info( 'Find %i ads on the page' % len(ads) )
      for ad in ads:
        preview = dict() 
        for field in self.preview_fields:
          try:
            preview[ field.name ] = getattr( self.field_types, field.type )( field, ad )  
          except Exception as e:
            #logging.exception(e)
            logging.warning( 'Field: wrong xpath %s %s. Parsing %s adware.' % (self.name, field.name, preview.get('url', 'don\'t know'))  )

        yield AttrDict(preview)

    else:
      logging.warning( 'Engine %s reach %i search page with "%s" query' \
                       % (self.name.capitalize(), self.max_seach_pages, query))


  def get_ad(self, url):
    pass

  
