#!/usr/bin/env python

import re
import json
from robobrowser import RoboBrowser

def get_table(table, key):
    data = {}
    header = table.find_all('tr', {'class': 'colhead'})[-1]
    rows = table('tr')
    names = [' '.join(td.strings) for td in header]
    for row in rows:
        rda = {}
        # print row
        for name, td in zip(names, row('td')):
            rda[name] = ' '.join(td.strings)
        if not key in rda:
            print key, rda
            continue
        data[rda[key]] = rda
    return data


def get_sos():
    return get_pages('http://espn.go.com/mens-college-basketball/rpi/_/year/2013/sort/sos')

def get_page(link):
    print 'getting', link
    b.open(link.format(''))
    table = b.find('table', {'class': 'tablehead'})
    data = get_table(table, u'TEAM')
    # get the next link
    numbers = b.find('div', {'class': 'page-numbers'})
    next = numbers.next_sibling
    while next.name not in ('a', 'div'):
        next = next.next_sibling
    if next.name == 'a':
        print ' > has next', next['href']
        return data, next['href']
    else:
        print ' > no next', next
    return data, None

def get_pages(link):
    data = {}
    while link is not None:
        nda, link = get_page(link)
        data.update(nda)
    return data

'''
    for i in range(i, number):
        lnk = link.format('page/%d/' % i)
        print lnk
        b.open(lnk)
        table = b.find('table', {'class': 'tablehead'})
        data.update(get_table(table, 'TEAM'))
    return data
    '''

def get_stats():
    stats = ['scoring-per-game', 'rebounds', 'free-throws', '3-points', 'assists', 'steals', 'blocks']
    base = 'http://espn.go.com/mens-college-basketball/statistics/team/_/stat/{}/year/2013'
    data = {}
    for stat in stats:
        for k, row in get_pages(base.format(stat)).items():
            if k not in data:
                data[k] = row
            else:
                data[k].update(row)
    return data

b = RoboBrowser(history=True)

def do_this():
    getters = [get_stats, get_sos]
    data = {}
    for getter in getters:
        for k, row in getter().items():
            if k not in data:
                data[k] = row
            else:
                data[k].update(row)
    return data


open('massixe.json', 'w').write(json.dumps(do_this()))

# vim: et sw=4 sts=4
