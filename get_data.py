#!/usr/bin/env python

import json

def get_stats(year):
    return json.loads(open('data/stats_{}.json'.format(year)).read())

def get_sos(year):
    return json.loads(open('data/sos_{}.json'.format(year)).read())

def get_data(year):
    stats = get_stats(year)
    sos = get_sos(year)
    alzz = {}
    for k, row in stats.items():
        if 'TEAM_ID' not in row: continue
        alzz[row['TEAM_ID']] = row
    for k, row in sos.items():
        if 'TEAM_ID' not in row: continue
        if row['TEAM_ID'] not in alzz:
            alzz[row['TEAM_ID']] = {}
        alzz[row['TEAM_ID']].update(row)
    return alzz

def get_results(year):
    return json.loads(open('data/results_{}.json'.format(year)).read())

def getDuo(val):
    '''take 23-34 => 23, 34'''
    one, two = val.split('-')
    return one, two

def get_attrs(data):
    v = data.values()[0]
    attrs = []
    for k,v in v.items():
        try:
            float(v)
        except:
            print 'skip attr', k, v
            continue
        attrs.append(k)
    return attrs


# vim: et sw=4 sts=4
