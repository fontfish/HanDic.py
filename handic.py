#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  handic.py, a handy Han dictionary for Mandarin learners who want an
#  easy offline dictionary on Linux.
#
#  Requires the CC-CEDICT file to work. Download here:
#  https://www.mdbg.net/chinese/dictionary?page=cedict
#
#  With thanks to MDBG online dictionary and the CC-CEDICT authors.
#
#  Disclaimer: I do not pretend that this is well-written Python, or
#  that it follows any Pythonic standard. It is a quick and dirty
#  solution to the lack of open source Chinese dictionaries available on
#  Linux.
#
#  Made by FontFish, August/September 2020
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import re

def user_input(dictfile, mode, searches):
    print("""
 SEARCH MODE: %s      -- Hanzi CEDICT viewer --       SEARCHES: %s
________________________________________________________________________
 *1 = Hanzi   *2 = Pinyin   *3 = Meaning   *4 = Pinyin Key   *Q  = Quit
""" % (mode, searches))
    uin = input(">>> ")
    if len(uin) > 0 and uin[0] == '*':
        if uin.lower() == '*h' or uin == '*1':
            mode = "Hanzi  "
        elif uin.lower() == '*p' or uin == '*2':
            mode = "Pinyin "
        elif uin.lower() == '*m' or uin == '*3':
            mode = "Meaning"
            print("""  Warning:
  Searching by meaning may bring up an unweildy number of results.
""")
        elif uin.lower() == '*k' or uin == '*4':
            print("""
------------------------------------------------------------------------
 Pinyin key:    1 = –     2 = /     3 = V     4 = \\     5 = blank tone
------------------------------------------------------------------------
""")
        elif uin.lower() == '*q':
            mode = "QUIT"
        result = {}
    elif len(uin) > 0:
        if mode == "Hanzi  ":
            result = search_hanzi(dictfile, uin)
        elif mode == "Pinyin ":
            result = search_pinyin(dictfile, uin)
        elif mode == "Meaning":
            result = search_meaning(dictfile, uin)
        if len(result) < 1:
            print()
            print("  No search results found.")
            print()
        searches += 1
    else:
        result = {}
    return mode, result, searches

# Alternative possible header.
"""
                       -- Hanzi CEDICT viewer --
------------------------------------------------------------------------
 *1 = Hanzi   *2 = Pinyin   *3 = Meaning   *4 = Pinyin Key   *Q  = Quit
________________________________________________________________________
       SEARCH MODE: %s                       SEARCHES: %s
"""

# It may be preferable to use the commented-out “line.find(query)” line if looking for an exact match,
# though the “x in line for x in query” search allows for the removal of separating dots:
# A search for “齊內丁齊達內” will still return “齊內丁·齊達內”, for instance.
def search_hanzi(dictfile, query):
    results = []
    with open(dictfile, 'r') as cedict:
        for line in cedict:
            line = line.rstrip()
            if line[0] != "#" and all(x in line for x in query):
#            if line[0] != "#" and line.find(query) >= 0:
                line = line.rstrip()
                han = line.replace('·', '').replace('・', '')# This line is of no use if using “line.find(query)”
                han = han.split(' ', 2)
                if han[0] == query or han[1] == query:
                    results.append(line)
    return results

def search_pinyin(dictfile, query):
    if len(query) > 0:
        results = []
        ql = query.lower().split()
        with open(dictfile, 'r') as cedict:
            for line in cedict:
                line = line.rstrip()
                occur = 0
                if line[0] != "#" and all(x in line.lower() for x in ql):
                    py = re.split(r'\[|\]', line.lower())[1]
                    py = py.replace('· ', '').replace('・', ' ')
                    py = py.split()
                    if len(py) == len(ql):
                        for p, q in zip(py, ql):
                            if q[-1].isdigit() and p == q:
                                occur += 1
                            elif p[-1].isdigit() and p[:-1] == q:
                                occur += 1
                            elif p == q:
                                occur += 1
                if occur == len(ql):
                    results.append(line)
        return results


def search_meaning(dictfile, query):
    results = []
    ql = query.lower().split()
    with open(dictfile, 'r') as cedict:
        for line in cedict:
            line = line.rstrip()
            if line[0] != "#" and all(x in line.lower() for x in ql):
                count = 0
                for q in ql:
                    if re.search(rf'\b{re.escape(q)}\b', line[line.find(']'):], re.IGNORECASE):
                        count += 1
                if count >= len(ql):
                    results.append(line)
        return results


def print_results(results):
    if len(results) > 0:
        print()
        for r in results:
            hanzi = r.split(' ',2)
            pinyin = hanzi[2][1:].split('] ')# Previously re.split(r'\[|\]\s', r[2][1:])
            meaning = pinyin[1].split('/')
            print()
            print("-------------------------")
            print()
            print("  " + hanzi[1] + "　（" + hanzi[0] + "）　" + pinyin[0])
            print()
            for i in meaning:
                if len(i) > 0 and not i.isspace():
                    print("  " + i.capitalize() + ".")
        print()
        print("-------------------------")
        print()

dictfile = "cedict_ts.u8"
mode = "Hanzi  "# "Pinyin " "Meaning"
searches = 0
uin = "0"
print("""
------------------------------------------------------------------------
Type an asterisk (*) followed by the search mode number to change mode.
------------------------------------------------------------------------
""")

while mode != "QUIT":
    mode, results, searches = user_input(dictfile, mode, searches)
    print_results(results)
