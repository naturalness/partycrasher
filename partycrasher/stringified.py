from partycrasher.crash import Stackframe

def stringify_value(v):
    """ Force ints/bools to strings for ES """
    if isinstance(v, list) and not isinstance(v, StringifiedList):
        return StringifiedList(v)
    elif isinstance(v, dict) and not isinstance(v, StringifiedDict):
        return StringifiedDict(v)
    elif isinstance(v, int):
        return str(v)
    elif isinstance(v, bool):
        return str(v)
    elif isinstance(v, float):
        return str(v)
    elif isinstance(v, bytes):
        # Force strings to be unicoded
        return v.decode(encoding='utf-8', errors='replace')
    else:
        return v
      
def fix_key_for_es(key):
    if isinstance(key, bytes):
        key = key.decode(encoding='utf-8', errors='replace')
    key = key.replace('.', '_')
    key = key.replace(':', '_')
    key = key.replace(' ', '_')
    return key

class StringifiedDict(dict):
    def __setitem__(self, key, val):
        # First force strings to be unicoded
        key = fix_key_for_es(key)
        
        val = stringify_value(val)
        #print("key: " + key + "val: " + repr(val), file=sys.stderr)
        if key == 'address':
            assert isinstance(val, string_types)

        return super(StringifiedDict, self).__setitem__(key, val)

    def normalize(self):
        """
        Checks ALL of the existing keys and remaps them to normalized values.

        Note that due to normalization, the keys may shift. That is, this
        condition does NOT hold.

            frame[key] = value
            frame[key] == value
        """
        # Use self.keys() so that we can remove items (it is impossible to
        # modify the dictionary during iteration).
        for key in self.keys():
            # __setitem__ WILL change the
            value = self[key]
            del self[key]
            self.__setitem__(key, value)

    def __init__(self, *args):
        super(StringifiedDict, self).__init__(*args)
        if not (len(args) == 1 and isinstance(args[0], self.__class__)):
            self.normalize()

class StringifiedList(list):
    
    def __init__(self, value=[], **kwargs):
        if isinstance(value, list):
            if len(value) == 0:
                return
            else:
                self.extend(value)
        else:
            raise AttributeError

    def extend(self, arg):
        return super(StringifiedList, self).extend(map(stringify_value, arg))

    def append(self, *args):
        return self.extend(args)

    def __setitem__(self, index, value):
        return super(StringifiedList, self).__setitem__(index, stringify_value(value))

    def __setslice__(self, i, j, seq):
        return super(StringifiedList, self).__setitem__(i, j, map(stringify_value, seq))

    def __eq__(self, other):
        return (super(StringifiedList, self).__eq__(other)
                and self.__class__ == other.__class__)

class Stacktrace(StringifiedList):

    stackframe_class = Stackframe

    """A list which can only contain stackframes..."""
    def __init__(self, value=[], **kwargs):
        if isinstance(value, list):
            if len(value) == 0:
                return
            else:
                self.extend(map(self.stackframe_class, value))
        else:
            raise AttributeError

    def extend(self, arg):
        for a in arg:
            assert isinstance(a, self.stackframe_class)
        return super(Stacktrace, self).extend(arg)

    def append(self, *args):
        return self.extend(args)

    def __setitem__(self, index, value):
        for v in value:
            assert isinstance(v, self.stackframe_class)
        return super(Stacktrace, self).__setitem__(index, value)

    def __setslice__(self, i, j, seq):
        for v in seq:
            assert isinstance(v, self.stackframe_class)
        return super(Stacktrace, self).__setitem__(i, j, seq)

    def __eq__(self, other):
        return (super(Stacktrace, self).__eq__(other)
                and self.__class__ == other.__class__)
