#!/usr/bin/env python

import re
import json
from robobrowser import RoboBrowser

def get_id(href):
    return int(href.split('/id/')[-1].split('/')[0])

def get_bracket_data(year):
    url = 'http://espn.go.com/mens-college-basketball/tournament/bracket/_/id/{}22/'.format(year)
    b = RoboBrowser()
    b.open(url)
    data = []
    for item in b.find_all(attrs={'class': 'match'}):
        t1, t2 = [(get_id(a['href']), a['title']) for a in item('a')]
        s1, s2 = ' '.join(item.find('dd').stripped_strings).split()
        data.append([t1, t2, s1, s2])
    return data


def get_bracket(year):
    print 'Getting', year
    data = get_bracket_data(year)
    fname = 'results_{}.json'.format(year)
    open(fname, 'w').write(json.dumps(data))

def main():
    [get_bracket(year) for year in range(2010, 2015)]

main()

# vim: et sw=4 sts=4
