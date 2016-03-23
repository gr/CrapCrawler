#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys 
import argparse 
import os
import yaml
import logging, logging.config

from crawler.common import AttrDict
from crawler.models import Manager
from crawler.models import Engine
from crawler.models import Field
from crawler.models import Search
from crawler.models import Contact
from crawler.models import get_session




def fill_db( db_path):
  logging.debug( 'Fill database' )
  session = get_session( db_path )

  m = Manager()
  m.name = 'George'
  m.contacts = [Contact(type='phone', contact='777')]
  session.add(m)

  e = Engine()
  e.name = 'avito'
  e.url = 'https://www.avito.ru/moskva?p=<pagination>&bt=1&q=<query>'
  e.delay = 5
  e.eop = '//div[@class="pagination__nav clearfix"]/a[@class="pagination__page"][2]'
  e.preview_price = True
  e.encoding = 'utf-8'
  e.fields = [Field('str', 'search','search',"//div[@class='item item_table clearfix js-catalog-item-enum c-b-0']",e),
              Field('str', 'preview', 'title', "div[@class='description']/h3/a", e),
              Field('url', 'preview', 'url', "div[@class='description']/h3/a", e),
              Field('price', 'preview', 'price', "div[@class='description']/div[@class='about']", e),
              Field('date', 'preview', 'date', "div/div/div[@class='date c-2']", e),
              Field('image', 'preview', 'img', "div[@class='b-photo']/a/img", e)]

  session.add(e)

  s = Search()
  s.name = 'yaesu'
  s.query = 'yaesu'
  s.min_price = 5000
  s.max_price = 15000
  s.enabled = True
  s.engines = [e]
  s.periodicity = 5
  s.manager = [m]
  s.notice_by = 'email'

  session.commit()



if __name__ == "__main__":
  cwd = os.path.dirname(os.path.abspath(__file__))
  db_path = cwd + '/run/db/crawler.sqlite3'


  fill_db( db_path )
   

