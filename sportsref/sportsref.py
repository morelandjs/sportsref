#!/usr/bin/env python3

from pathlib import Path
from xdg import XDG_DATA_HOME

import bs4
import pandas
import requests
import re


def findTables(url):
    """
    Provides a list of the html tables that can be found at the url
    provided. The order in the list returned should reflect the order
    that the tables appear. On pro-football-reference.com, these names
    usually indicate what information they contain.

    """
    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    divs = soup.findAll('div', id="content")
    divs = divs[0].findAll("div", id=re.compile("^all"))

    ids = []
    for div in divs:
        searchme = str(div.findAll("table"))
        x = searchme[searchme.find("id=") + 3: searchme.find(">")]
        x = x.replace("\"", "")
        if len(x) > 0:
            ids.append(x)

    return ids

def pullTable(url, tableID, header=True):
    """
    Pulls a table (indicated by tableID, which can be identified with
    "findTables") from the specified url. The header option determines
    if the function should try to determine the column names and put
    them in the returned data frame. The default for header is True.
    If you get an index error for data_header, try specifying header =
    False. I will include a generated error message for that soon.

    """
    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    tables = soup.findAll('table', id=tableID)
    data_rows = tables[0].findAll('tr')

    game_data = [
        [td.getText() for td in data_rows[i].findAll(['th','td'])]
        for i in range(len(data_rows))
    ]

    data = pandas.DataFrame(game_data)

    if header == True:
        data_header = tables[0].findAll('thead')
        data_header = data_header[0].findAll("tr")
        data_header = data_header[0].findAll("th")

        header = []
        for i in range(len(data.columns)):
            header.append(data_header[i].getText())

        data.columns = header
        data = data.loc[data[header[0]] != header[0]]

    data = data.reset_index(drop=True)

    return data


if __name__ == "__main__":
    import argparse

    cachedir = Path(XDG_DATA_HOME, 'sportsref')
    cachedir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect('sportsref.db')
