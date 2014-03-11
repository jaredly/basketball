#!/usr/bin/env python


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
        id = getId(name)
        if id is False:
            print 'Have id-less team'
            id = gs(name)
        won = gs(row.find('li', {'class': 'game-status'})).lower() == 'w'
        data[id] = [gs(name), won, gs(score)]
    print ' > got', len(data)
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

# vim: et sw=4 sts=4
