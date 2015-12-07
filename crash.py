#  Copyright (C) 2015 Jshua Charles Campbell

import UserDict, UserList

class Stackframe(dict):
  pass
  
class Stacktrace(list):
  """A list which can only contain stackframes..."""
  
  def __init__(self, value=[], **kwargs):
    if isinstance(value, list):
      if len(value) == 0:
        return
      else:
        self.extend(map(Stackframe, value))
    else:
      raise AttributeError
  
  def extend(self, arg):
    for a in arg:
      assert isinstance(a, Stackframe)
    return super(ucSource, self).extend(arg)

  def append(self, *args):
    return self.extend(args)

  def __setitem__(self, index, value):
    for v in value:
      assert isinstance(v, Stackframe)
    return super(Stacktrace, self).__setitem__(index, value)
  
  def __setslice__(self, i, j, seq):
    for v in seq:
      assert isinstance(v, Stackframe)
    return super(Stacktrace, self).__setitem__(i, j, seq)

class Crash(dict):
  
  synonyms = {
    'crash_id' => 'database_id', # Mozilla
    'ProblemType' => 'type', # Apport
    'DistroRelease' => 'os', # Apport
    'ProcVersionSignature' => 'os_version', # Apport
    'os_ver' => 'os_version', # Mozilla
    'cpu_arch' => 'cpu', # Mozilla
    'Architecture' => 'cpu', # Apport
    'frames' => 'stacktrace', # Mozilla
  }
  breakapart = {
    'crash_info' => 1, # Mozilla
    'system_info' => 1, # Mozilla
  }

  def __init__(self, *args):
    super(Crash, self).__init__(*args)
    self.normalize()
   
  def __setitem__(self, key, val):
    if key in synonyms:
       super(Crash, self).__setitem__(synonyms[key], val)
    elif key in breakapart:
      if isinstance(val, dict):
        for key2 in val:
          self.__setitem__(key2, val[key2])
      else:
        raise ValueError("Expected a dict!")
    elif key == 'Date': # Apport
      self.__setitem__('date', datetime('val'))
    elif key == 'crashing_thread': # Mozilla
      if (isinstance(val, dict)):
        for key2 in val:
          self.__setitem__(key2, val[key2])
      elif:
        super(Crash, self).__setitem__(key, val)
      
  def normalize(self):
    for key in self.keys():
      value = self[value]
      del self[value]
      self.__setitem__(key, value)

class TestCrash(unittest.TestCase):
  def test_mozilla(self):
    
  