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

def user_input(mode, searches):
    print("""
MODE: %s            SEARCHES: %s
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
        elif uin.lower() == '*k' or uin == '*4':
            print()
            print("Pinyin key:   1 = –     2 = /     3 = V     4 = \\     5 = blank tone")
            print()
        elif uin.lower() == '*q':
            mode = "QUIT"
        result = {}
    elif len(uin) > 0:
        if mode == "Hanzi  ":
            result = search_hanzi(uin)
        elif mode == "Pinyin ":
            result = search_pinyin(uin)
        elif mode == "Meaning":
            result = search_meaning(uin)
        searches += 1
    else:
        result = {}
    return mode, result, searches

def search_hanzi(query):
    newvar = 0
    results = {}
    with open("cedict_ts.u8", 'r') as cedict:
        for line in cedict:
            if line[0] != "#" and line.find(query) >= 0:
                line = re.split(r'\[|\]', line)
                hanzi = line[0].split()
                if hanzi[0] == query or hanzi[1] == query:
                    results[newvar] = line
                    newvar += 1
    return results


def search_pinyin(query):
    if len(query) > 0:
        newvar = 0
        results = {}
        ql = query.lower().split()
        with open("cedict_ts.u8", 'r') as cedict:
            for line in cedict:
                count = 0
                if line[0] != "#" and all(x in line for x in ql):
                    line = re.split(r'\[|\]', line)
                    py = line[1].split()
                    if len(py) == len(ql):
                        for p, q in zip(py, ql):
                            if p == q or re.match(rf'{re.escape(q)}\d', p, re.IGNORECASE):
                                count += 1
                if count == len(ql):
                    results[newvar] = line
                    newvar += 1
        return results


def search_meaning(query):
    newvar = 0
    results = {}
    ql = query.split()
    with open("cedict_ts.u8", 'r') as cedict:
        for line in cedict:
            if line[0] != "#" and all(x in line for x in ql):
                count = 0
                line = re.split(r'\[|\]', line)
                for q in ql:
                    if re.search(rf'\b{re.escape(q)}\b', line[2], re.IGNORECASE):
                        count += 1
                if count == len(ql):
                    results[newvar] = line
                    newvar += 1
        return results


def print_results(result):
    if len(result) > 0:
        for l in result:
            hanzi = result[l][0].split()
            print()
            print()
            print("-------------------------")
            print()
            print(hanzi[1] + "  （" + hanzi[0] + "）  " + result[l][1])
            print("")
            print(result[l][2])
        print()
        print("-------------------------")
        print()


mode = "Hanzi  "# "Pinyin " "Meaning"
searches = 0
uin = "0"
print("""
------------------------------------------------------------------------
Type an asterisk (*) followed by the search mode number to change mode.
------------------------------------------------------------------------
""")

while mode != "QUIT":
    mode, result, searches = user_input(mode, searches)
    print_results(result)
