# -*- coding: utf-8 -*-

from itertools import product
from datetime import datetime
import pandas as pd

from sportsref import pullTable, findTables


baseurl = 'https://www.pro-football-reference.com/'

def games(season_min, season_max):
    """
    Return all NFL games for the specified years

    """
    def get_table(season):
        url = baseurl + f"years/{season}/games.htm"
        df = pullTable(url, "games")

        df.columns = [
            'week',
            'day',
            'date',
            'time',
            'winner_team',
            'location',
            'loser_team',
            'boxscore',
            'winner_score',
            'loser_score',
            'winner_yards',
            'winner_turnovers',
            'loser_yards',
            'loser_turnovers',
        ]

        df = df[df.week != '']
        df.drop(columns='boxscore', axis=1, inplace=True)

        for key in 'winner_team', 'loser_team':
            df[key] = df[key].str.rpartition(' ')[2]

        def teams(row):
            suffixes = ('team', 'score', 'yards', 'turnovers')

            if '@' in row['location']:
                prefixes = [('home', 'loser'), ('away', 'winner')]
            elif 'N' in row['location']:
                prefixes = [('home', 'loser'), ('away', 'winner')]
            else:
                prefixes = [('home', 'winner'), ('away', 'loser')]

            new_columns = {
                f'{p1}_{s}': row[f'{p2}_{s}']
                for (p1, p2), s in product(prefixes, suffixes)
            }

            return new_columns

        new_entries = df.apply(lambda row: teams(row), axis=1)
        new_df = df.from_records(new_entries)
        df = pd.concat([df.reset_index(), new_df], axis=1)

        def add_year(date):
            month, day = date.split()
            year = season if month in ['January', 'February'] else season + 1
            return date + ', {}'.format(year)

        df.date = df.date.apply(add_year)

        return df

    for season in range(season_min, season_max + 1):
        try:
            df = df.append(get_table(season))
        except NameError:
            df = get_table(season)

    return df

games = games(2006, 2018)
print(games)
