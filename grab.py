#!/usr/bin/env python

import re
import json
from robobrowser import RoboBrowser

def get_table(table, key, more=None):
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
        if more:
            more(rda, row)
        data[rda[key]] = rda
    return data

def more_id(rda, row):
    ids = row['class'][-1].split('-')[-1]
    try:
        id = int(ids)
    except:
        return
    rda['TEAM_ID'] = id

def get_sos(year=2014):
    return get_pages('http://espn.go.com/mens-college-basketball/rpi/_/year/{}/sort/sos'.format(year), more_id)

def get_page(link, more=None):
    print 'getting', link
    b.open(link.format(''))
    # get the next link
    numbers = b.find('div', {'class': 'page-numbers'})
    next = numbers.next_sibling
    while not hasattr(next, 'name') or next.name not in ('a', 'div'):
        next = next.next_sibling
    table = b.find('table', {'class': 'tablehead'})
    data = get_table(table, u'TEAM', more)
    if next.name == 'a':
        print ' > has next', next['href']
        return data, next['href']
    else:
        print ' > no next', next
    return data, None

def get_pages(link, more=None):
    data = {}
    while link is not None:
        nda, link = get_page(link, more)
        data.update(nda)
    return data

def gs(what):
    return ' '.join(what.strings)

def getId(haslinks):
    a = haslinks.find('a')
    if not a:
        print haslinks
        return False
    return int(a['href'].split('/id/')[1].split('/')[0])

def get_stats(year):
    stats = ['scoring-per-game', 'rebounds', 'free-throws', '3-points', 'assists', 'steals', 'blocks']
    base = 'http://espn.go.com/mens-college-basketball/statistics/team/_/stat/{}/year/{}'
    data = {}
    for stat in stats:
        for k, row in get_pages(base.format(stat, year), more_id).items():
            if k not in data:
                data[k] = row
            else:
                data[k].update(row)
    return data

b = RoboBrowser(history=True)

def do_this(what):
    getters = [get_sos, get_stats]
    getters.pop(0 if what else 1)
    data = {}
    for getter in getters:
        for k, row in getter().items():
            if k not in data:
                data[k] = row
            else:
                data[k].update(row)
    return data

# raw = json.dumps(do_this(False))
# open('sched-id.json', 'w').write(raw)

def save_stats(year):
    fname = 'stats_{}.json'.format(year)
    print 'getting', fname
    raw = json.dumps(get_stats(year))
    open(fname, 'w').write(raw)


def save_sos(year):
    fname = 'sos_{}.json'.format(year)
    print 'getting', fname
    raw = json.dumps(get_sos(year))
    open(fname, 'w').write(raw)

def main():
    [save_stats(year) for year in range(2010, 2015)]
    # [save_sos(year) for year in range(2010, 2015)]

main()

# vim: et sw=4 sts=4
