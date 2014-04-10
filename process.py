#!/usr/bin/env python

import random
import json

from get_data import get_data, get_results, getDuo, get_attrs

def chooseSos(sos1, sos2, *a):
    return sos1 > sos2

def chooseRandom(*a):
    return random.random() > .5

def chooseName(s1, s2, c1, c2, d1, d2):
    return d1['TEAM'] > d2['TEAM']

def noOrder(*a):
    return True

orderings = {
    'arbitrary': chooseName,
    'feature-based': chooseSos,
    'duplication': False,
    'random': chooseRandom
}

def oneline(data, attrs, id1, name1, sc1, id2, name2, sc2, rightOrder):
    # print id1, id2
    sos1 = int(data[id1]['SOS'])
    sos2 = int(data[id2]['SOS'])
    sc1 = int(sc1)
    sc2 = int(sc2)
    d1 = data[id1]
    d2 = data[id2]

    if not rightOrder(sos1, sos2, sc1, sc2, d1, d2):
        sos1, sos2 = sos2, sos1
        sc1, sc2 = sc2, sc1
        name1, name2 = name2, name1
        id1, id2 = id2, id1
        d1, d2 = d2, d1

    line = []
    line.append(json.dumps(d1['TEAM']))
    line.append(json.dumps(d2['TEAM']))
    line.append(str(sc1))
    line.append(str(sc2))
    def diff(attr):
        # print attr, d2[attr], d1[attr]
        if attr == 'TEAM': return
        if attr not in d1 or attr not in d2: return '?'
        return float(d2[attr]) - float(d1[attr])
    # for attr in attrs:
        # line.append(str(diff(attr)))
    for attr in attrs:
        line.append(str(d1.get(attr, '?')))
    line += list(getDuo(d1.get('FTM-FTA', '0-0')))
    for attr in attrs:
        line.append(str(d2.get(attr, '?')))
    line += list(getDuo(d2.get('FTM-FTA', '0-0')))
    line.append('WIN' if sc1 > sc2 else 'LOSS')
    return line

def csvHead(attrs, out):
    out.write('\t'.join(['index', 'rev', 'team1','team2', 'score1', 'score2'] +
        [n.replace('%', '__')+'1' for n in attrs] + ['FTMa1', 'FTAa1'] + 
        [n.replace('%', '__')+'2' for n in attrs] + ['FTMa2', 'FTAa2'] + 
        ['outcome']) + '\n')

def arffHead(attrs, out):
    out.write('@attribute index numeric\n')
    out.write('@attribute rev {NORM,REV}\n')
    out.write('@attribute team1 string\n')
    out.write('@attribute team2 string\n')
    out.write('@attribute score1 numeric\n')
    out.write('@attribute score2 numeric\n')
    for attr in attrs:
        out.write('@attribute {}1 numeric\n'.format(attr.replace('%', '__')))
    for attr in attrs:
        out.write('@attribute {}2 numeric\n'.format(attr.replace('%', '__')))
    out.write('@attribute outcome {WIN,LOSS}\n')
    out.write('@data\n')

def main(name, ordering, csv=False):
    years = range(2010, 2015)
    out = open(name + '.' + ('csv' if csv else 'arff'), 'w')
    if not csv:
        out.write('@relation basketball\n')
    datas = [get_data(year) for year in years]
    attrs = get_attrs(datas[0])
    print 'Using', attrs
    if csv:
        csvHead(attrs, out)
    else:
        arffHead(attrs, out)

    i = 0
    Is = range(265)
    for year in years:
        data = get_data(year)
        results = get_results(year)
        for ((id1, name1), (id2, name2), sc1, sc2) in results:
            if id1 not in data:
                print 'Team not found', id1
                continue
            if id2 not in data:
                print 'Team not found', id2
                continue

            i = random.choice(Is)
            Is.remove(i)

            if ordering == False:
                line_norm = [str(i), 'NORM'] + oneline(data, attrs, id1, name1, sc1, id2, name2, sc2, noOrder)
                out.write(('\t' if csv else ',').join(line_norm) + '\n')
                line_rev = [str(i), 'REV'] + oneline(data, attrs, id2, name2, sc2, id1, name1, sc1, noOrder)
                out.write(('\t' if csv else ',').join(line_rev) + '\n')
            else:
                line_norm = [str(i), 'NORM'] + oneline(data, attrs, id1, name1, sc1, id2, name2, sc2, ordering)
                out.write(('\t' if csv else ',').join(line_norm) + '\n')

    out.close()

def gen_all():
    for k, v in orderings.items():
        main(k, v, True)

main('double-mix', False, True)


# vim: et sw=4 sts=4
