#!/usr/bin/python
# -*- coding: utf-8 -*-

from engine import Engine
from models import Engine as ORM_Engine 
from models import Search, sqlite_session  


searches = sqlite_session.query( Search ) .all()

print '\n'.join(( s.name for s in searches ))




