# encoding: utf-8
"""A JSON store to use in place of shelve. Unicode keys, FTW!

This is for small stores. Everything is in memory and sync() always writes
everything out to disk.
"""

# Copyright (c) 2010-2013 Jeremy Avnet
# Copyright (c) 2016 Joshua Charles Campbell

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import
from __future__ import unicode_literals

__version__ = "2.1"

import __builtin__
import os
import shutil
from tempfile import NamedTemporaryFile
import UserDict

try:
    import simplejson as json
except ImportError:
    import json


class JSONStore(UserDict.DictMixin):

    def __init__(self, path, json_kw=None, mode=0600, object_hook=None):
        """Create a JSONStore object backed by the file at `path`.

        If a dict is passed in as `json_kw`, it will be used as keyword
        arguments to the json module.
        """
        self.path = path
        self.json_kw = json_kw or {}
        self.mode = mode
        self.object_hook = object_hook

        self._data = {}

        self._synced_json_kw = None
        self._needs_sync = False

        if not os.path.exists(path):
            self.sync(force=True)  # write empty dict to disk
            return

        # load the whole store
        with __builtin__.open(path, 'r') as fp:
            self.update(json.load(fp, object_hook=self.object_hook))

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        self._needs_sync = True

    def __delitem__(self, key):
        del self._data[key]
        self._needs_sync = True

    def keys(self):
        return self._data.keys()

    def _mktemp(self):
        prefix = os.path.basename(self.path) + "."
        dirname = os.path.dirname(self.path)
        return NamedTemporaryFile(prefix=prefix, dir=dirname, delete=False)

    def sync(self, json_kw=None, force=False):
        """Atomically write the entire store to disk if it's changed.

        If a dict is passed in as `json_kw`, it will be used as keyword
        arguments to the json module.

        If force is set True, a new file will be written even if the store
        hasn't changed since last sync.
        """
        json_kw = json_kw or self.json_kw
        if self._synced_json_kw != json_kw:
            self._needs_sync = True

        if not (self._needs_sync or force):
            return False

        with self._mktemp() as fp:
            json.dump(self._data, fp, **json_kw)
            os.fsync(fp.fileno())
        if self.mode != 0600:  # _mktemp uses 0600 by default
            os.chmod(fp.name, self.mode)
        shutil.move(fp.name, self.path)

        self._synced_json_kw = json_kw
        self._needs_sync = False
        return True


open = JSONStore
