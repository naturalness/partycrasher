#!/usr/bin/env python

import json
import sys
from pprint import pprint

with open(sys.argv[1]) as f:
    pprint(json.loads(f.read()))
