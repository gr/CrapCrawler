# -*- coding: utf-8 -*-

import logging, logging.config
import re

class FieldTypes():

  def url(self, field, ad):
    return self.str( field, ad )


  def str(self, field, ad):
    return ad.xpath( field.xpath )[0].text.strip()


  def int(self, field, ad):
    number = ad.xpath( field.xpath )[0].text.strip()
    number = re.findall('\d+', number)
    number = '0' + ''.join(number)
    return int(number)


  def date(self, field, ad):
    return self.str( field, ad )


  def price(self, field, ad):
    return self.int( field, ad )

  def image(self, field, ad):
    return self.str( field, ad )










#class Avito():
#  base = 'https://www.avito.ru/'  
#  place = 'moskva'
#  preview_price = True
#  encoding = 'utf-8'
#  max_search_pages = 100
#
#  def __init__(self):
#    logging.debug('Initialize Avito driver')
#    logging.debug('Base: %s, place: %s' % (self.base, self.place) )
#
#
#  def get_search_pages(self, query):
#    for x in xrange(1, self.max_search_pages):
#      url = "%s%s?p=%i&q=%s"% (self.base, self.place, x, query)
#      r = requests.get( url )
#      if r.status_code == 200:
#        logging.debug( 'Get %i bytes' % len(r.content) )
#        yield r.content.decode( self.encoding )
#      else:
#        logging.debug( 'Response code: %i; stop paginating' %r.status_code )
#        break
#      
#
#  months = ('zero', u'января', u'февраля', u'марта',        \
#           u'апреля', u'мая', u'июня', u'июля', u'августа', \
#           u'сентября', u'октября', u'ноября', u'декабря')
#
#
#  def str2date(self, str):
#    str = date.today().strftime('%Y ') + str.replace(u' в ', u' ').lower()
#
#    if u'сегодня' in str or u'вчера' in str:
#      str = str.replace(u'сегодня', date.today().strftime('%d %m') )
#      str = str.replace(u'вчера', (date.today() - td(days=1)).strftime('%d %m'))
#    else:
#      m = str.split()[2]
#      str = str.replace( m, '%02d' % self.months.index(m) )
#
#    return dt.strptime(str, '%Y %d %m %H:%M')
#
#
#  def search(self, query):
#    logging.debug('Processing query: %s' % query)
#    for page in self.get_search_pages( query ):
#      tree = fromstring(page)                  
#      ads = tree.xpath( "//div[@class='item item_table clearfix js-catalog-item-enum c-b-0']" )
#      logging.debug( 'Find %i results on page' % len(ads) )
#      for ad in ads:
#        preview = dict() 
#        title = ad.xpath( "div[@class='description']/h3/a" )[0]
#        preview['title'] = title.text.strip()
#
#        preview['url']   = title.get('href')
#        if not self.base in preview['url']:
#          preview['url'] = self.base + preview['url'][1:]
#
#        preview['price'] = ad.xpath( "div[@class='description']/div[@class='about']" )[0].text
#        preview['price'] = int( '0' + ''.join(preview['price'].split()[:-1]) )
#        
#        preview['date'] = ad.xpath( "div/div/div[@class='date c-2']")[0].text.strip()
#        preview['date'] = self.str2date( preview['date'] )
#
#        try:
#          preview['img'] = ad.xpath( "div[@class='b-photo']/a/img" )[0].get('src')[2:]
#        except:
#          preview['img'] = ''
#
#        yield AttrDict(preview)
#
#
