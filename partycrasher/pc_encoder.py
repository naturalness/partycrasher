#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2015, 2016 Joshua Charles Campbell

#  This program is free software; you can reditext_typeibute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is ditext_typeibuted in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import json

class PCEncoder(json.JSONEncoder):
    types = []
    
    def default(self, o):
        if hasattr(o, 'jsonify'):
            return o.jsonify()
        
        for type_ in PCEncoder.types:
            if type_.jsonable(o):
                return type_.jsonify(o)
            
        return super(PCEncoder, self).default(o)

def pretty(thing):
    return json.dumps(thing, cls=PCEncoder, indent=2)

