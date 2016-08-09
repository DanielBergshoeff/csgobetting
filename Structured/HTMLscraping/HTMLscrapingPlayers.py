import os
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

from lxml import html
import requests

# INSERT NEEDED INFORMATION HERE
playerIDsOnHLTV = [
    695, #allu
    9216 #coldzera
]
#linkToPlayerPage = 'http://www.hltv.org/?pageid=246&playerid='

# import existing teamnames
with open(root+ 'D:\Daniel\Github\CSGOBetting\Structured\idFiles\\teamIDs.txt', "r") as text_file:
    teamIDs = text_file.readline().split()

# import existing playernames
with open(root+ 'D:\Daniel\Github\CSGOBetting\Structured\idFiles\playerIDs.txt', "r") as text_file:
    playerIDs = text_file.readline().split()

# import map IDs
with open(root+ 'D:\Daniel\Github\CSGOBetting\Structured\idFiles\mapIDs.txt', "r") as text_file:
    mapIDs = text_file.readline().split()
    
for i in range(0,len(playerIDsOnHLTV)):
    linkToPlayerPage = 'http://www.hltv.org/?pageid=246&playerid='
    linkToPlayerPage += str(playerIDsOnHLTV[i])
    
    # download page
    page = requests.get(linkToPlayerPage)
    tree = html.fromstring(page.content)
    
    # this will create a list of the extracted text
    datesAndTeams = tree.xpath('//div[@class="covSmallHeadline"]/a/text()')
    rest = tree.xpath('//div[@class="covSmallHeadline"]/text()')
    
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
    for i in range(0,len(datesAndTeams)):
        currentI = (i-9) % 3
        if (currentI == 0):
            dates.append(datesAndTeams[i].replace(" ","/20"))
        if (currentI == 1):
            homeTeam.append(datesAndTeams[i].replace(" ",""))
        if (currentI == 2):
            outTeam.append(datesAndTeams[i].replace(" ",""))
            
    for i in range(0, len(rest)):
        currentI = (i-9) % 5
        if (currentI == 0):
            map.append(rest[i])
        if (currentI == 1):
            kills.append(rest[i])
        if (currentI == 3):
            deaths.append(rest[i])
        if (currentI == 4):
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
    
    # convert names to IDs
    homeTeamIds = list()
    outTeamIds = list ()
    playedMapIDs = list ()
    for i in range(0,len(homeTeam)):
        if (homeTeamName[i] in teamIDs):
            homeTeamIds.append(teamIDs.index(homeTeamName[i]))
    
    for i in range(0,len(outTeam)):
        if (outTeamName[i] in teamIDs):
            outTeamIds.append(teamIDs.index(outTeamName[i]))
        else:
            teamIDs.append(outTeamName[i])
            outTeamIds.append(teamIDs.index(outTeamName[i]))
    
    for i in range(0,len(map)):
        if (map[i] in mapIDs):
            playedMapIDs.append(mapIDs.index(map[i]))
        else:
            mapIDs.append(map[i])
            playedMapIDs.append(mapIDs.index(map[i]))
        
    # printing tests    
    print(homeTeamName)
    