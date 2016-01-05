#!/usr/bin/env python

#  Copyright (C) 2015 Joshua Charles Campbell

#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

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
        return super(Stacktrace, self).extend(arg)

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
        'crash_id': 'database_id', # Mozilla
        'os_ver' : 'os_version', # Mozilla
        'cpu_arch' : 'cpu', # Mozilla
        'frames' : 'stacktrace', # Mozilla
    }
    breakapart = {
        'crash_info' : 1, # Mozilla
        'system_info' : 1, # Mozilla
    }

    def __init__(self, *args):
        super(Crash, self).__init__(*args)
        self.normalize()

    @classmethod
    def load_from_file(cls, path):
        import launchpad_crash
        crash_classes = [ launchpad_crash.LaunchpadCrash ]
        
        crash = None
        for crash_class in crash_classes:
            try:
                crash = crash_class.load_from_file(path)
            except NotImplementedError:
                raise
            else:
                break
        if crash is None:
            raise NotImplementedError("I don't know how to load this!")
        return crash

    def __setitem__(self, key, val):
        synonyms = self.synonyms
        if key in synonyms:
            return super(Crash, self).__setitem__(synonyms[key], val)
        elif key in self.breakapart:
            if isinstance(val, dict):
                for key2 in val:
                    self.__setitem__(key2, val[key2])
            else:
                raise ValueError("Expected a dict!")
        elif key == 'crashing_thread': # Mozilla
            if (isinstance(val, dict)):
                for key2 in val:
                    self.__setitem__(key2, val[key2])
            else:
                raise ValueError("Expected a dict!")
        else:
            return super(Crash, self).__setitem__(key, val)
        
    def normalize(self):
        for key in self.keys():
            value = self[value]
            del self[value]
            self.__setitem__(key, value)
    

