#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2015, 2016 Joshua Charles Campbell

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

from six import string_types
import re
from partycrasher.pc_exceptions import BadProjectNameError

good = re.compile('(\w+)$')

class Project(object):
    """
    Metadata about a project.
    """
    name = None
    
    def __init__(self, project):
        if isinstance(project, Project):
            self.name == project.name
        elif isinstance(project, string_types):
            self.name = project
        elif isinstance(project, dict) and 'name' in project:
            self.name = project['name']
        else:
            raise BadProjectNameError(repr(self.name))
        m = good.match(self.name)
        if m is None:
            raise BadProjectNameError(self.name)
        if m.group(1) != self.name:
            raise BadProjectNameError(self.name)
    
    def __str__(self):
        return self.name
