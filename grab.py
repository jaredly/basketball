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

def more_schedule(rda, row):
    ids = row['class'][-1].split('-')[-1]
    try:
        id = int(ids)
    except:
        return
    print row['class'], ids, id
    rda['2014-schedule'] = get_schedule(id)
    rda['2013-schedule'] = get_schedule(id, 2013)
    rda['TEAM_ID'] = id

def get_sos():
    return get_pages('http://espn.go.com/mens-college-basketball/rpi/_/year/2013/sort/sos', more_schedule)

def get_page(link, more=None):
    print 'getting', link
    b.open(link.format(''))
    # get the next link
    numbers = b.find('div', {'class': 'page-numbers'})
    next = numbers.next_sibling
    while next.name not in ('a', 'div'):
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

def get_schedule(id, year=None):
    base = 'http://espn.go.com/mens-college-basketball/team/schedule/_/id/{}/'
    if year:
        base += 'year/%s/' % year
    print 'getting schedule', base.format(id)
    b.open(base.format(id))
    table = b.find('div', {'id': 'showschedule'}).find('table')
    data = {}
    for row in table('tr'):
        if 'oddrow' not in row['class'] and 'evenrow' not in row['class']: continue
        name = row.find('li', {'class': 'team-name'})
        score = row.find('li', {'class': 'score'})
        if not name or not score: continue
        data[gs(name)] = gs(score)
    print ' > got', len(data)
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
    getters = [get_sos, get_stats]
    data = {}
    for getter in getters:
        for k, row in getter().items():
            if k not in data:
                data[k] = row
            else:
                data[k].update(row)
    return data

raw = json.dumps(do_this())
open('scheduled.json', 'w').write(raw)

# vim: et sw=4 sts=4
