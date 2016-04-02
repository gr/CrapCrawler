        fill_orm_titlewords( preview, session )
    


        #if  engine.preview_price and preview.price > 0:
        #  fill_orm_titlewords(preview, session)

        #if search.price_min <= preview.price <= search.price_max or not engine.preview_price:
        #  ad = engine.get_ad( preview.url )
        #  if not engine.preview_price and ad.price > 0:
        #    fill_orm_titlewords(ad, session)

        #  if search.price_min <= ad.price <= search.price_max:
        #    orm_ad = fill_orm_ad(ad, session)
        #    orm_ad.rating = 0



class Word(Base):
  __tablename__ = 'words'

  id         = Column(Integer, primary_key=True)
  word       = Column(String(50))
  popularity = Column(Float)

  def __repr__(self):
    return "<Word (id=%i, word=%s)>" % (self.id, self.word)




def fill_orm_ad( ad, session ):
  orm_ad = session.query(Ad).filter( Ad.url == ad.url ).first()
  if not orm_ad:
    orm_ad = Ad(url=ad.url)

  for k,v in ad.items():
    setattr(orm_ad, k ,v)

  session.add(orm_ad)
  session.flush()
  return orm_ad


def fill_orm_titlewords( ad, session ):
  orm_ad = fill_orm_ad(ad, session)

  for word in ad.title.split():

    word = word.lower()
    orm_word = session.query(Word).filter( Word.word == word ).first()
    if not orm_word:
      orm_word = Word()
      orm_word.word = word
      orm_word.ads = [orm_ad]
    
    if not orm_ad in orm_word.ads:
      orm_word.ads.append(orm_ad)

    session.add(orm_word)
    session.flush()

    prices = [ x.price for x in orm_word.ads ]
    logging.debug( str(prices) )
    prices = map(lambda x: int(x), prices)
    prices.sort()
    mediane = prices[ len(prices)/2 ]
    diff = map(lambda x: x - mediane, prices)
    sq_diff = reduce(lambda x,y: x+y*y, diff, 0) / len(prices)
    sqrt_diff = math.sqrt(sq_diff)
    
    orm_word.popularity = float(sqrt_diff) / (mediane +1)
  
    session.add(orm_word)
    session.commit()

