# -*- coding: utf-8 -*-

from .main import pullTable


baseurl = 'https://www.basketball-reference.com/'

nba_season = [
    'october',
    'november',
    'december',
    'january',
    'february',
    'march',
    'april',
    'may',
    'june',
]

def games(year_min, year_max):
    """
    Return all NBA games for the specified years

    """
    for year in range(year_min, year_max + 1):
        for month in nba_season:
            url = baseurl + f"leagues/NBA_{year}_games-{month}.html"
            try:
                table = table.append(pullTable(url, "schedule"))
            except NameError:
                table = pullTable(url, "schedule")

    drop_cols = [6, 7, 8, 9]
    table.drop(table.columns[drop_cols], axis=1, inplace=True)

    table.columns = [
        'date',
        'time',
        'away_team',
        'away_points',
        'home_team',
        'home_points',
    ]

    return table
