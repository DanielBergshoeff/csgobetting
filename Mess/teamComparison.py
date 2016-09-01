import numpy as np
from datetime import date

# INSERT NEEDED INFORMATION HERE
fileToImport = 'matchesTotal.txt'
timeWeightLoss = -0.3
daysBackLimit = 100

# import data from import file
import_data = np.genfromtxt(fileToImport,delimiter = ',')

import_dates = import_data[:,][:,0:3]
import_homeTeamName = import_data[:,][:,3]
import_homeTeamScore = import_data[:,][:,4]
import_outTeamName = import_data[:,][:,5]
import_outTeamScore = import_data[:,][:,6]
import_map = import_data[:,][:,7]
import_event = import_data[:,][:,8]

# import team IDs
with open('teamIDs.txt', "r") as text_file:
    teamIDs = text_file.readline().split()
    
# import map IDs
with open('mapIDs.txt', "r") as text_file:
    mapIDs = text_file.readline().split()
    
# import event IDs
with open('eventIDs.txt', "r") as text_file:
    eventIDs = text_file.readline().split()


# turn to representation functions    
def teamIDtoName (id):
    return teamIDs[int(id)]
def teamNametoID (name):
    return teamIDs.index(name)

def mapIDtoName (id):
    return mapIDs[int(id)]
def mapeNametoID (name):
    return mapIDs.index(name)

def eventIDtoName (id):
    return eventIDs[int(id)]


# calculations for time-balancing
def daysSinceGame (gameDate, nextGameDate):
    d0 = date(int(gameDate[0]),int(gameDate[1]),int(gameDate[2]))
    d1 = date(int(nextGameDate[0]),int(nextGameDate[1]), int(nextGameDate[2]))
    delta = d1 - d0
 #   if (delta.days < 0):
 #       print ("WARNING: DAYCOUNT IS NEGATIVE, WRONG DATE?")
    return delta.days

def effectOnNextGame (gameDate, nextGameDate):
    timePast = daysSinceGame(gameDate, nextGameDate)
    return pow(timePast, timeWeightLoss)

def getGameResult(homeTeamScore, outTeamScore):
    homeTeamScore = int(homeTeamScore)
    outTeamScore = int(outTeamScore)
    if (homeTeamScore > outTeamScore):
        return 1
    else:
        return 0

def getWinLoseRatioVS (teamName1, teamName2, nextGameDate):
    divider = 0
    gamesScore = 0
    gamesPlayed = 0
    team1ID = teamNametoID (teamName1)
    team2ID = teamNametoID (teamName2)
    for i in range (0,len(import_dates)):
        if (daysSinceGame(import_dates[i], nextGameDate) < daysBackLimit and daysSinceGame(import_dates[i],nextGameDate) > 0):
            
            if(import_homeTeamName[i] == team1ID and import_outTeamName[i] == team2ID):
                effect = effectOnNextGame(import_dates[i],nextGameDate)
                divider += 1 * effect
                gamesPlayed += 1
                gameResult = getGameResult(import_homeTeamScore[i], import_outTeamScore[i])
                if (gameResult > 0):
                    gamesScore += gameResult * effect
            
            if(import_homeTeamName[i] == team2ID and import_outTeamName[i] == team1ID):
                effect = effectOnNextGame(import_dates[i],nextGameDate)
                divider += 1 * effect
                gamesPlayed += 1
                gameResult = getGameResult(import_outTeamScore[i], import_homeTeamScore[i])
                if (gameResult > 0):
                    gamesScore += gameResult * effect
        
    if (divider > 0):
        return [gamesScore / divider, gamesPlayed]
    else:
        return 'invalid'

def getWinLoseRatioMap (teamName1, map,nextGameDate):
    divider = 0
    gamesScore = 0
    gamesPlayed = 0
    team1ID = teamNametoID(teamName1)
    mapID = mapeNametoID (map)
    for i in range (0,len(import_dates)):
        if (daysSinceGame(import_dates[i],nextGameDate) < daysBackLimit and daysSinceGame(import_dates[i],nextGameDate) > 0):
            
            if (import_homeTeamName[i] == team1ID and import_map[i] == mapID):
                effect = effectOnNextGame(import_dates[i],nextGameDate)
                divider += 1 * effect
                gamesPlayed += 1
                gameResult = getGameResult(import_homeTeamScore[i], import_outTeamScore[i])
                if (gameResult > 0):
                    gamesScore += gameResult * effect
            
            if (import_outTeamName[i] == team1ID and import_map[i] == mapID):
                effect = effectOnNextGame(import_dates[i],nextGameDate)
                divider += 1 * effect
                gamesPlayed += 1
                gameResult = getGameResult(import_outTeamScore[i], import_homeTeamScore[i])
                if (gameResult > 0):
                    gamesScore += gameResult * effect
        
    if (divider > 0):
        return [gamesScore / divider, gamesPlayed]
    else:
        return 'invalid'
    
def getWinLoseRatioMapVS (teamName1, teamName2, map,nextGameDate):
    divider = 0
    gamesScore = 0
    gamesPlayed = 0
    team1ID = teamNametoID(teamName1)
    team2ID = teamNametoID(teamName2)
    mapID = mapeNametoID (map)
    for i in range (0,len(import_dates)):
        if (daysSinceGame(import_dates[i],nextGameDate) < daysBackLimit and daysSinceGame(import_dates[i],nextGameDate) > 0):
            
            if (import_homeTeamName[i] == team1ID and import_outTeamName[i] == team2ID and import_map[i] == mapID):
                effect = effectOnNextGame(import_dates[i],nextGameDate)
                divider += 1 * effect
                gamesPlayed += 1
                gameResult = getGameResult(import_homeTeamScore[i], import_outTeamScore[i])
                if (gameResult > 0):
                    gamesScore += gameResult * effect
            
            if (import_homeTeamName[i] == team2ID and import_outTeamName[i] == team1ID and import_map[i] == mapID):
                effect = effectOnNextGame(import_dates[i],nextGameDate)
                divider += 1 * effect
                gamesPlayed += 1
                gameResult = getGameResult(import_outTeamScore[i], import_homeTeamScore[i])
                if (gameResult > 0):
                    gamesScore += gameResult * effect
        
    if (divider > 0):
        return [gamesScore / divider, gamesPlayed]
    else:
        return 'invalid'

def getRatios (team1, team2, map, date):
    print ('Win / lose ratio of {0} against {1}: {2}'.format(
        team1,
        team2,
        getWinLoseRatioVS(team1,team2, date)))
    print ('Win / lose ratio of {0} on {1}: {2}'.format(
        team1,
        map,
        getWinLoseRatioMap(team1,map, date)))
    print ('Win / lose ratio of {0} on {1}: {2}'.format(
        team2,
        map,
        getWinLoseRatioMap(team2,map, date)))
    print ('Win / lose ratio of {0} against {1} on {2}: {3}'.format(
        team1,
        team2,
        map,
        getWinLoseRatioMapVS(team1,team2,map, date)))
    print ("-----------------------------")
    
getRatios('Astralis', 'EnVyUs', 'train',[2016,7,24])