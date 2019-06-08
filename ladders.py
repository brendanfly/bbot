import urllib.request
from bs4 import BeautifulSoup

"""Crawls the warlight webpage"""
ladder_pageurls = ['http://md-ladder.cloudapp.net/']
for ladder_pageurl in ladder_pageurls:
    ladder_page = urllib.request.urlopen(ladder_pageurl)
    soup = BeautifulSoup(ladder_page, 'html.parser')
    tables = soup.find_all('table')

    header_str = soup.title.string.split("-")
    print("__" + header_str[0].strip() + "__")

    data = ""
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            for column in columns:
                if column.contents[0].strip() and "Rank" in column.contents[0].strip():
                    found_table = True
                    break
                elif len(columns) == 3:
                    rating_column = columns[2]
                    team_column = columns[1]
                    data = columns[0].contents[0].strip()
                    data += ") "
                    current_link = 0
                    for link in team_column.find_all('a'):
                        if "playerId" in link.get('href'):
                            if (link.contents[0].strip()) != "":
                                data += link.contents[0].strip() + " "
                            current_link += 1
                            if (current_link > 1) and (current_link < len(columns)):
                                data += "/ "

                    data += " Rating: " + rating_column.contents[0]
            print(data)
        if found_table:
            found_table = False
            print("")
            print("==========================================")
            print("")
            break
