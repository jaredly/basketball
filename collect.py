#!/usr/bin/env python
import json

schedule = json.loads(open('./Schedule.json').read())
stats = json.loads(open('./stats-id.json').read())

def didWin(text):
    a,b = map(str, text.split('-'))
    return a > b

items = {}
for dct in schedule.values():
    if 'TEAM_ID' not in dct:
        continue
    for k,v in dct['2013-schedule'].items():
        dct['v-13-%d' % k] = didWin(v)
    items[dct['TEAM_ID']] = dct

for dct in stats.values():
    if 'TEAM_ID' not in dct:
        continue
    if dct['TEAM_ID'] not in items:
        items[dct['TEAM_ID']] = {}
    items[dct['TEAM_ID']].update(dct)

values = list(items.values())
cols = set(values[0].keys())
for v in values[:5]:
    cols = cols.union(set(v.keys()))
cols = list(cols)


import csv
with open('all.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, cols)
    [writer.writerow(row) for row in values]


# vim: et sw=4 sts=4
