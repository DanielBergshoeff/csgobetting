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

linkToMatchesPage = 'http://www.hltv.org/match/2304000-virtuspro-nip-esl-pro-league-season-4-europe'
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

    import_data.append(np.genfromtxt(matchfile, delimiter = ','))
    
import_dates = import_data[0][:,][:,0:3]
import_times = import_data[0][:,][:,3]
import_homeTeamID = import_data[0][:,][:,4]
import_outTeamID = import_data[0][:,][:,5]
import_mapID = import_data[0][:,][:,6]
import_eventID = import_data[0][:,][:,7]
import_homeTeamScore = import_data[0][:,][:,8]
import_outTeamScore = import_data[0][:,][:,9]
import_homeTeamCTRounds = import_data[0][:,][:,10]
import_outTeamTRounds = import_data[0][:,][:,11]
import_homeTeamTRounds = import_data[0][:,][:,12]
import_outTeamCTRounds = import_data[0][:,][:,13]
import_playerTeamID = import_data[0][:,][:,14]
import_playerKills = import_data[0][:,][:,15]
import_playerDeaths = import_data[0][:,][:,16]
import_playerRating = import_data[0][:,][:,17]

print(import_playerRating[0])

'''plt.plot(import_playerKills, import_playerDeaths)
plt.show()'''

        
print('DONE')