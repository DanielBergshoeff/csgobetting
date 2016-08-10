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

from lxml import html
import requests


linkToTop20Page = 'http://www.hltv.org/ranking/teams/'

# download page
page = requests.get(linkToTop20Page)
tree = html.fromstring(page.content)

# this will create a list of the extracted text
allLinks = tree.xpath('//a[@class="noCollapseLink"]/@href')
allTeamNames = tree.xpath('//div[@class="ranking-teamName"]/a/text()')
allNickNames = tree.xpath('//div[@class="ranking-playerNick"]/a/text()')

teamLinks = list()
teamIDs = list()
playerLinks = list()
playerIDs = list ()

for i in range(0,len(allLinks)):
    if ( i % 11 != 10):
        playerLinks.append(allLinks[i])
    else:
        teamLinks.append(allLinks[i])

for i in range(0,len(teamLinks)):
    teamID = teamLinks[i].split("=")[2]
    teamIDs.append([allTeamNames[i], teamID])


for i in range(0,len(playerLinks),2):
    if (playerLinks[i][:2] == '/?'):
        playerID = playerLinks[i].split("=")[2]
        playerIDs.append([allNickNames[i/2].strip(), playerID])
    else:
        playerID = playerLinks[i].split("/")[2]
        playerIDs.append([allNickNames[i/2].strip(), playerID.split("-")[0]])

# write everything to file

# import ID files
if platform == "darwin":
    # OS X
    filename = root+ 'idFiles/HLTV_players.txt'
    with open(filename, "w+") as text_file:
        for i in range(0,len(playerIDs)):
            text_file.write("{0}, {1}\n".format(
                playerIDs[i][0], playerIDs[i][1]))
    filename = root+ 'idFiles/HLTV_top20Teams.txt'
    with open(filename, "w+") as text_file:
        for i in range(0,len(teamIDs)):
            text_file.write("{0}, {1}\n".format(
                teamIDs[i][0], teamIDs[i][1]))
elif platform == "win32" or platform == "cygwin":
    # Windows
    filename = root+ 'idFiles\\HLTV_players.txt'
    with open(filename, "w+") as text_file:
        for i in range(0,len(playerIDs)):
            text_file.write("{0}, {1}\n".format(
                playerIDs[i][0], playerIDs[i][1]))
    filename = root+ 'idFiles\\HLTV_top20Teams.txt'
    with open(filename, "w+") as text_file:
        for i in range(0,len(teamIDs)):
            text_file.write("{0}, {1}\n".format(
                teamIDs[i][0], teamIDs[i][1]))

    
print ("DONE")