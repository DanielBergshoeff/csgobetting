import os

from sys import platform
if platform == "darwin":
    # OS X
    script_dir = os.path.dirname(__file__)
    script_dirArray = script_dir.split("/")
    structuredPos = 0
    root = ''
    for i in range(len(script_dirArray)-1,0,-1):
        if(script_dirArray[i] == 'Structured'):
            structuredPos = i + 1
    for i in range(0,structuredPos):
        root += script_dirArray[i]
        root += '/'
    import sys
    sys.path.append('/usr/local/lib/python2.7/site-packages')
elif platform == "win32" or platform == "cygwin":
    # Windows...
    script_dir = os.path.dirname(__file__)
    script_dirArray = script_dir.split("\\")
    structuredPos = 0
    root = ''
    for i in range(len(script_dirArray)-1,0,-1):
        if(script_dirArray[i] == 'Structured'):
            structuredPos = i + 1
    for i in range(0,structuredPos):
        root += script_dirArray[i]
        root += '\\'

import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

from lxml import html
import requests

# import player ID's
if platform == "darwin":
    # OS X
    with open(root+ 'idFiles/HLTV_players.txt', "r") as text_file:
        allPlayersHLTV = text_file.read().split('\n')
elif platform == "win32" or platform == "cygwin":
    # Windows
    with open(root+ 'idFiles\\HLTV_players.txt', "r") as text_file:
        allPlayersHLTV = text_file.read().split('\n')

# import ID files
if platform == "darwin":
    # OS X
    with open(root+ 'idFiles/teamIDs.txt', "r") as text_file:
        teamIDs = text_file.readline().split()
    with open(root+ 'idFiles/mapIDs.txt', "r") as text_file:
        mapIDs = text_file.readline().split()
    with open(root+ 'idFiles/eventIDs.txt', "r") as text_file:
        eventIDs = text_file.readline().split()
elif platform == "win32" or platform == "cygwin":
    # Windows
    with open(root+ 'idFiles\\teamIDs.txt', "r") as text_file:
        teamIDs = text_file.readline().split()
    with open(root+ 'idFiles\\mapIDs.txt', "r") as text_file:
        mapIDs = text_file.readline().split()
    with open(root+ 'idFiles\\eventIDs.txt', "r") as text_file:
        eventIDs = text_file.readline().split()
        
    
for l in range(0,len(allPlayersHLTV)):
    linkToPlayerPage = 'http://www.hltv.org/?pageid=246&playerid='
    playerID = allPlayersHLTV[l].replace(" ", "").split(",")
    linkToPlayerPage += str(playerID[1])
    
    # download page
    page = requests.get(linkToPlayerPage)
    tree = html.fromstring(page.content)
    
    # this will create a list of the extracted text
    rest = tree.xpath('//div[@class="covSmallHeadline"]//text()')
    
    # create lists
    dates = list()
    date_year = list ()
    date_month = list ()
    date_day = list ()
    
    homeTeam = list()
    homeTeamName = list()
    homeTeamScore = list()
    
    outTeam = list()
    outTeamName = list()
    outTeamScore = list()
    
    map = list()
    
    kills = list()
    deaths = list()
    rating = list()
    
    # split and process collected list to individual lists
    for i in range(10,len(rest)):
        currentI = (i - 10) % 9
        if (currentI == 0):
            dates.append(rest[i].replace(" ","/20"))
        elif (currentI == 1):
            homeTeam.append(rest[i].replace(" ",""))
        elif (currentI == 2):
            outTeam.append(rest[i].replace(" ",""))
        elif (currentI == 3):
            map.append(rest[i])
        elif (currentI == 4):
            kills.append(rest[i])
        elif (currentI == 6):
            deaths.append(rest[i])
        elif (currentI == 8):
            rating.append(rest[i])
            
    # split date
    for i in range(0,len(dates)):
        date_year.append(dates[i].split("/")[2])
        date_month.append(dates[i].split("/")[1])
        date_day.append(dates[i].split("/")[0])
        
    # split scores from teamnames
    for i in range(0,len(homeTeam)):
        homeTeamName.append(homeTeam[i].split("(")[0])
        homeTeamScore.append(homeTeam[i].split("(")[1].replace(")",""))
        outTeamName.append(outTeam[i].split("(")[0])
        outTeamScore.append(outTeam[i].split("(")[1].replace(")",""))
            
    # write everything to file
    playerName = playerID[0]
    playerName += '.txt'
    
    if platform == "darwin":
        # OS X
        filename = root + 'playerMatchFiles/matches_'
    elif platform == "win32" or platform == "cygwin":
        # Windows
        filename = root + 'playerMatchFiles\\matches_'

    filename += playerName
    with open(filename, "w+") as text_file:
        for i in range(0,len(dates)):
            text_file.write("{0},{1},{2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10} \n".format(
                date_year[i], str(date_month[i]).zfill(2), str(date_day[i]).zfill(2),
                str(homeTeamName[i]).zfill(3),
                str(homeTeamScore[i]).zfill(2),
                str(outTeamName[i]).zfill(3),
                str(outTeamScore[i]).zfill(2),
                str(map[i]).zfill(2),
                str(kills[i]).zfill(2),
                str(deaths[i]).zfill(2),
                str(rating[i]).zfill(3)))                

print('DONE')    