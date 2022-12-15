#!/usr/bin/env python3
import os
import re
import sys

DEBUG   = False
VERSION = '0.1'
SNAPSHOTS = []
DB = dict()

def db_get(line):
    cmd, var = re.split(r'\s+', line, 1)
    if var in DB:
        return DB[var]
    return 'NULL'

def db_set(line):
    global DB
    cmd, var, val = re.split(r'\s+', line, 2)
    DB[var] = val
    return val

def db_unset(line):
    global DB
    cmd, var = re.split(r'\s+', line, 1)
    if var in DB:
        del DB[var]
    return

def db_find(line):
    cmd, val = re.split(r'\s+', line, 1)
    count = 0
    found = []
    for k in DB:
        if DB[k] == val:
            count = count + 1
            found.append(k)

    found.sort()
    return ",".join(found)

def db_counts(line):
    cmd, val = re.split(r'\s+', line, 1)
    count = 0
    for k in DB:
        if DB[k] == val:
            count = count + 1

    return count

def db_dump():
    global DB
    print(DB)
    return

def db_begin():
    global SNAPSHOTS, DB
    SNAPSHOTS.append(DB.copy())
    if DEBUG: print("SNAPSHOTS: ", SNAPSHOTS)
    return

def db_commit():
    global SNAPSHOTS, DB
    SNAPSHOTS = []
    return

def db_rollback():
    global SNAPSHOTS, DB
    if len(SNAPSHOTS) > 0:
        DB = SNAPSHOTS.pop()
    if DEBUG: print("SNAPSHOTS: ", SNAPSHOTS)
    return

def main():
    print(f"test-pydb server {VERSION}. Type 'end' or Ctrl-D to exit.")
    if DEBUG: print(f"Debug mode is On")

    for line in sys.stdin:
        line = line.rstrip()
        if 'end' == line.lower():
            break

        if DEBUG: print(f'Processing {line}')

        if re.match(r'get\s+', line):
            print(db_get(line))

        if re.match(r'set\s+', line):
            db_set(line)

        if re.match(r'unset\s+', line):
            db_unset(line)

        if re.match(r'find\s+', line):
            print(db_find(line))

        if re.match(r'counts\s+', line):
            db_counts(line)

        if re.match(r'begin\s*', line):
            db_begin()

        if re.match(r'rollback\s*', line):
            db_rollback()

        if re.match(r'commit\s*', line):
            db_commit()

        if re.match(r'dump\s*', line):
            db_dump()

    print("Bye.")

if __name__ == "__main__":
    main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4:
