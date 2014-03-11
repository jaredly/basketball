#!/usr/bin/env python

import json

def get_stats(year):
    return json.loads(open('stats_{}.json'.format(year)).read())

def get_sos(year):
    return json.loads(open('sos_{}.json'.format(year)).read())

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
    return json.loads(open('results_{}.json'.format(year)).read())

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

def main(csv=False):
    years = range(2010, 2015)
    out = open('data.' + ('csv' if csv else 'arff'), 'w')
    if not csv:
        out.write('@relation basketball\n')
    datas = [get_data(year) for year in years]
    attrs = get_attrs(datas[0])
    print 'Using', attrs
    if csv:
        out.write('\t'.join(['team1','team2', 'score1', 'score2'] + [n+'1' for n in attrs] + [n+'2' for n in attrs] + ['outcome']) + '\n')
    else:
        out.write('@attribute team1 string\n')
        out.write('@attribute team2 string\n')
        out.write('@attribute score1 numeric\n')
        out.write('@attribute score2 numeric\n')
        for attr in attrs:
            out.write('@attribute {}1 numeric\n'.format(attr))
        for attr in attrs:
            out.write('@attribute {}2 numeric\n'.format(attr))
        out.write('@attribute outcome {WIN,LOSS}\n')
        out.write('@data\n')
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
            sos1 = int(data[id1]['SOS'])
            sos2 = int(data[id2]['SOS'])
            if sos1 > sos2:
                sc1, sc2 = sc2, sc1
                name1, name2 = name2, name1
                id1, id2 = id2, id1
            sc1 = int(sc1)
            sc2 = int(sc2)
            d1 = data[id1]
            d2 = data[id2]
            line = []
            line.append(json.dumps(d1['TEAM']))
            line.append(json.dumps(d2['TEAM']))
            line.append(str(sc1))
            line.append(str(sc2))
            for attr in attrs:
                line.append(str(d1.get(attr, '?')))
            for attr in attrs:
                line.append(str(d2.get(attr, '?')))
            line.append('WIN' if sc1 > sc2 else 'LOSS')
            out.write(('\t' if csv else ',').join(line) + '\n')
    out.close()


main(False)


# vim: et sw=4 sts=4
