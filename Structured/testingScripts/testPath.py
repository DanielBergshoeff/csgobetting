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

import csv
import numpy as np
import matplotlib.pyplot as plt

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

'''linkToMatchesPage = 'http://www.hltv.org/match/2304000-virtuspro-nip-esl-pro-league-season-4-europe'
# download page
page = requests.get(linkToMatchesPage)
tree = html.fromstring(page.content)
    
# this will create a list of the extracted text    
rest = tree.xpath('//div[@class="text-center"]//text()')

players = [rest[1], rest[3], rest[5], rest[7], rest[9], rest[11], rest[13], rest[15], rest[17], rest[19]]
import_data = list()

print(players[3])

for i in range(0, len(players)):
    importfile = root + "playerMatchFiles\\matches_"
    playerfile =  players[i].replace(" ", "") + ".txt"
    matchfile = importfile + playerfile

    import_data.append(np.genfromtxt(matchfile, delimiter = ','))'''
    
import_data = list()
matchfile = root + "playerMatchFiles\\all_matches.txt"    
import_data.append(np.genfromtxt(matchfile, delimiter = ','))

for i in range(0, len(import_data[0])):
    import_matchPlayer1ID

import_matchID = import_data[0][:,][:,0]
import_matchPlayer1ID = import_data[0][:,][:,1]
import_matchPlayer2ID = import_data[0][:,][:,2]
import_matchPlayer3ID = import_data[0][:,][:,3]
import_matchPlayer4ID = import_data[0][:,][:,4]
import_matchPlayer5ID = import_data[0][:,][:,5]
import_matchPlayer6ID = import_data[0][:,][:,6]
import_matchPlayer7ID = import_data[0][:,][:,7]
import_matchPlayer8ID = import_data[0][:,][:,8]
import_matchPlayer9ID = import_data[0][:,][:,9]
import_matchPlayer10ID = import_data[0][:,][:,10]
import_matchYear = import_data[0][:,][:,11]
import_matchMonth = import_data[0][:,][:,12]
import_matchDay = import_data[0][:,][:,13]
import_matchTimeHours = import_data[0][:,][:,14]
import_matchTimeMinutes = import_data[0][:,][:,15]
import_matchTeam1ID = import_data[0][:,][:,16]
import_matchTeam2ID = import_data[0][:,][:,17]
import_matchMapID = import_data[0][:,][:,18]
import_matchEventID = import_data[0][:,][:,19]
import_matchScoreTeam1 = import_data[0][:,][:,20]
import_matchScoreTeam2 = import_data[0][:,][:,21]
import_matchScoreTeam1CT = import_data[0][:,][:,22]
import_matchScoreTeam2T = import_data[0][:,][:,23]
import_matchScoreTeam1T = import_data[0][:,][:,24]
import_matchScoreTeam2CT = import_data[0][:,][:,25]

print(import_matchPlayer2ID[2])

"dfsdf".replace("[", "").replace("]", "").strip()
'''plt.plot(import_playerKills, import_playerDeaths)
plt.show()'''

        
print('DONE')