#!/usr/bin/env python

# Copyright 2015 Joshua Charles Campbell

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

import MySQLdb
from sys import argv
import re, os, shutil, errno


def f1(seq):
   # not order preserving
   set = {}
   map(set.__setitem__, seq, [])
   return set.keys()


def main():
    db = MySQLdb.connect("localhost", "bicho", argv[1], "bicho")
    bugkets = dict()
    bugs_to_bugkets = dict()
    next_bugketid = 1
    new_bugket = True
    while new_bugket:
        new_bugket = False
        cursor = db.cursor()
        cursor.execute("SELECT lp_id, duplicate_of, duplicates_list FROM issues_ext_launchpad NATURAL JOIN issues;")
        for row in cursor:
            #print repr(row)
            lp_ids = [row[0]]
            if row[1] is not None:
                lp_ids.append(row[1])
            if row[2] is not None:
                lp_ids.extend([int(bugid) for bugid in row[2].split()])
            destination_bugkets = set()
            for bugid in lp_ids:
                if bugid in bugs_to_bugkets:
                    destination_bugkets.add(bugs_to_bugkets[bugid])
            if len(destination_bugkets)>0:
                bugket_id = next(iter(destination_bugkets))
                if len(destination_bugkets)>1:
                    print repr(destination_bugkets)
                    new_bugket = True
            else:
                bugket_id = next_bugketid
                next_bugketid = next_bugketid + 1
                new_bugket = True
                print "New: %i" % (bugket_id)
            for bugid in lp_ids:
                bugs_to_bugkets[bugid] = bugket_id
    for k, v in bugs_to_bugkets.iteritems():
        bugkets[v] = bugkets.get(v, [])
        bugkets[v].append(k)
    cursor = db.cursor()
    cursor.execute("SELECT name, url, lp_id, issues.description FROM issues_ext_launchpad INNER JOIN issues INNER JOIN attachments ON (attachments.issue_id = issues.id AND issues_ext_launchpad.issue_id = issues.id);")
    for row in cursor:
        name, url, bugid, description = row
        if re.search('CoreDump', name, flags=re.IGNORECASE):
            continue
        bugket_id = bugs_to_bugkets[bugid]
        str_bugid = "%010i" % (bugid)
        str_bugketid = "%09i" % (bugket_id)
        path = "bugkets/" + str_bugketid + "/" + str_bugid
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise
        i = 0
        filepath = path + "/" + name
        bugpath = re.sub('https://', '', url)
        while os.path.isfile(filepath):
            i = i+1
            filepath = path + "/" + name + "." + str(i)
        try:
            shutil.copyfile(bugpath, filepath)
            print filepath
        except IOError as exc: # Python >2.5
            if exc.errno == errno.ENOENT and os.path.isdir(path):
                pass
            else: raise
        postpath = path + "/Post.txt"
        if not os.path.isfile(postpath): # we get this multiple times due to our join denormalizing
            with open(postpath, "w") as post_file:
                post_file.write(description)
                print postpath


if __name__ == "__main__":
    main()