import pandas as pd
import numpy as np

#Team.factor = Team.park_road_ops / average_road_ops

data = pd.read_csv('Statcast_2021.csv')
teams = ['ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CWS', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KC', 'LAA', 'LAD', 'MIA', 'MIL', 'MIN', 'NYM', 'NYY', 'OAK', 'PHI', 'PIT', 'SD', 'SF', 'SEA', 'STL', 'TB', 'TEX', 'TOR', 'WSH']

class Team:
    def __init__(self, name):
        self.park_road_ops = 0
        self.name = name
        self.park_factor = 0
        self.calc_ops()

    #def __init__(self, name, park_road_ops, park_factor):
    #    self.name = name
    #    self.park_road_ops = park_road_ops
    #    self.park_factor = park_factor

    def calc_ops(self):
        #Clean Data
        df = data[['events', 'home_team', 'away_team', 'inning_topbot']]
        df = df[(df['home_team'] == self.name) & (df['inning_topbot'] == 'Top')].fillna(0)
        df = df[df['events'] != 0]
        #print(df)

        #Calculate Vistor On Base
        PA = df['events'].count()
        reached_base = df[(df['events'] == 'hit_by_pitch') | (df['events'] == 'walk') | (df['events'] == 'single') | (df['events'] == 'double') | (df['events'] == 'triple') | (df['events'] == 'home_run')]
        reached_base = reached_base['events'].count()
        obp = reached_base / PA
        #print(obp)

        #Calculate Vistor Slug
        AB = df[(df['events'] != 'hit_by_pitch') & (df['events'] != 'walk') & (df['events'] != 'sac_fly') & (df['events'] != 'sac_bunt')]
        AB = AB['events'].count()
        singles = df[df['events'] == 'single']
        singles = singles['events'].count()
        doubles = df[df['events'] == 'double']
        doubles = doubles['events'].count()
        triples = df[df['events'] == 'triple']
        triples = triples['events'].count()
        home_runs = df[df['events'] == 'home_run']
        home_runs = home_runs['events'].count()
        total_bases = singles + doubles * 2 + triples * 3 + home_runs * 4
        slug = total_bases / AB
        #print(slug)

        #Calculate OPS
        self.park_road_ops = obp + slug
        print(self.name, ': ', self.park_road_ops)


def calc_avg_visitor_ops():
    total_ops = 0
    for i in range(len(teams)):
        curr = Team(teams[i])
        total_ops = total_ops + curr.park_road_ops

    avg_ops = total_ops / 30
    return avg_ops


def calc_park_factor():
    avg_ops = calc_avg_visitor_ops()
    teams_list = []
    for i in range(len(teams)):
        curr = Team(teams[i])
        curr.park_factor = round((curr.park_road_ops / avg_ops) * 100)
        teams_list.append(curr)

    return teams_list

def determine_batting_team(row):
    if row['inning_topbot'] == 'Bot':
        return row['home_team']
    else:
        return row['away_team']

def stats_chart():
    df = data[['events', 'des', 'home_team', 'away_team', 'inning_topbot']].fillna(0)
    df = df[df['events'] != 0]
    
    #Create Hitting Team Variable
    df['batting_team'] = df.apply(determine_batting_team, axis=1)

    #Extract Batter Name from Description
    df['batter_name'] = [i.split()[0:2] for i in df['des']]
    df['batter_name'] = [' '.join(i) for i in df['batter_name']]
    
    t = df[['batter_name','batting_team']]
    t = df.groupby(['batter_name'])

    print(t)

    df = df[['events', 'batter_name']]
    df = df.sort_values(by=['batter_name'])
    
    singles = df[df['events'] == 'single']
    singles = singles.rename(columns={'events': '1B'})
    singles = singles.groupby(['batter_name']).count()
    doubles = df[df['events'] == 'double']
    doubles = doubles.rename(columns={'events': '2B'})
    doubles = doubles.groupby(['batter_name']).count()
    triples = df[df['events'] == 'triple']
    triples = triples.rename(columns={'events': '3B'})
    triples = triples.groupby(['batter_name']).count()
    home_runs = df[df['events'] == 'home_run']
    home_runs = home_runs.rename(columns={'events': 'HR'})
    home_runs = home_runs.groupby(['batter_name']).count()
    hit_by_pitches = df[df['events'] == 'HBP']
    hit_by_pitches = hit_by_pitches.rename(columns={'events': 'HBP'})
    hit_by_pitches = hit_by_pitches.groupby(['batter_name']).count()
    walks = df[df['events'] == 'walk']
    walks = walks.rename(columns={'events': 'BB'})
    walks = walks.groupby(['batter_name']).count()
    sac_flys = df[df['events'] == 'sac_fly']
    sac_flys = sac_flys.rename(columns={'events': 'SF'})
    sac_flys = sac_flys.groupby(['batter_name']).count()
    sac_bunts = df[df['events'] == 'sac_bunt']
    sac_bunts = sac_bunts.rename(columns={'events': 'SB'})
    sac_bunts = sac_bunts.groupby(['batter_name']).count()

    stats = df.groupby(['batter_name']).count()
    stats = stats.rename(columns={'events': 'PA', 'batting_team': 'TEAM'})
    stats['AB'] = stats['PA']
    stats = stats.merge(singles, on='batter_name', how='left').merge(doubles, on='batter_name', how='left').merge(triples, on='batter_name', how='left').merge(home_runs, on='batter_name', how='left')
    stats = stats.merge(walks, on='batter_name', how='left').merge(hit_by_pitches, on='batter_name', how='left').merge(sac_flys, on='batter_name', how='left').merge(sac_bunts, on='batter_name', how='left').fillna(0)

    stats['AB'] = stats['PA'] - stats['HBP'] - stats['BB'] - stats['SF'] - stats['SB']
    stats = stats.astype(int)
    
    stats['AVG'] = ((stats['1B'] + stats['2B'] + stats['3B'] + stats['HR']) / stats['AB']).round(3).fillna(0)
    stats['OBP'] = ((stats['1B'] + stats['2B'] + stats['3B'] + stats['HR'] + stats['HBP'] + stats['BB']) / stats['PA']).round(3).fillna(0)
    stats['SLG'] = ((stats['1B'] + 2 * stats['2B'] + 3 * stats['3B'] + 4 * stats['HR']) / stats['AB']).round(3).fillna(0)
    stats['OPS'] = (stats['OBP'] + stats['SLG']).round(3)

    stats = stats[stats['PA'] > 502]
    stats = stats.sort_values(by=['OPS'])


    print(stats)








def main():
    #avg_ops = calc_avg_visitor_ops()
    #teams_list = calc_park_factor()

    #print(teams_list[0].park_factor)

    stats_chart()



main()
