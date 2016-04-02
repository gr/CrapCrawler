# -*- coding: utf-8 -*-



# Helper class. access to dict elements as attr
class AttrDict(dict):
  def __init__(self, *args, **kwargs):
    super(AttrDict, self).__init__(*args, **kwargs)
    self.__dict__ = self

    for k, v in self.items():
      if isinstance(v, dict):
        self.__dict__[k] = AttrDict(v)

