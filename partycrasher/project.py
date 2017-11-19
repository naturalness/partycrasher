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
from partycrasher.pc_exceptions import BadProjectNameError, BadKeyNameError
from partycrasher.pc_type import (
    PCType,
    PCMaybeType,
    PCMultiType,
    key_type
    )

class Project(object):
    """
    Metadata about a project.
    """
    __slots__ = ('name',)
    
    def __init__(self, project):
        if isinstance(project, Project):
            self.name = project.name
        else:
            try:
                self.name = key_type(project)
            except BadKeyNameError as e:
                raise BadProjectNameError(repr(project))
    
    def __str__(self):
        return self.name
    
    def __copy__(self):
        return Project(self)
    
    def __hash__(self):
        return hash((Project, self.name))
    
    def __eq__(self, other):
        return isinstance(other, Project) and self.name == other.name
    
    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.name) + ")"
    
    def jsonify(self):
        return self.name

mustbe_project = PCType(checker=Project, converter=Project)

maybe_project = PCMaybeType(checker=Project, converter=Project)

multi_project = PCMultiType(Project, Project)
