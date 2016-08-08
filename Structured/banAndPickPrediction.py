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

import numpy as np
from datetime import date
from operator import itemgetter
import pdb

# INSERT NEEDED INFORMATION HERE
fileToImport = root+'matchFiles/matchesTotal.txt'
timeWeightLoss = -0.14
# -0.15 voor BO3 (0.29 correctness)
# -0.3 voor BO1 (0.29 correctness)

#daysBackLimit = 100

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
with open(root+'idFiles/teamIDs.txt', "r") as text_file:
    teamIDs = text_file.readline().split()
    
# import map IDs
with open(root+'idFiles/mapIDs.txt', "r") as text_file:
    mapIDs = text_file.readline().split()
    
# import event IDs
with open(root+'idFiles/eventIDs.txt', "r") as text_file:
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
        if (homeTeamScore - outTeamScore > 9):
            return 2
        else:
            return 1
    else:
        return 0

def getWinLoseRatioMap (teamName1, map,nextGameDate, daysBackLimit):
    divider = 0
    gamesScore = 0
    gamesPlayed = 0
    team1ID = teamNametoID(teamName1)
    mapID = mapeNametoID (map)
    for i in range (0,len(import_dates)):
        if (daysSinceGame(import_dates[i],nextGameDate) < daysBackLimit and daysSinceGame(import_dates[i],nextGameDate) > 0):
            
            if (import_homeTeamName[i] == team1ID and import_map[i] == mapID): # bool voor home / out, rest is hetzelfde
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
        
    if (gamesPlayed > 0):
        return [gamesScore / divider, gamesPlayed]
    else:
        return [0,0]
    
def probableMapBan (results): # [team1ratio, aantal spellen team 1, team2ratio, aant spel 2, map]
    results.sort(key=itemgetter(0))
    numResults = len(results)
    for i in range (0,len(results)):
        if ((results[i][1] - results[i][3]) < -5 and (results[i][0] - results[i][2]) < -0.2): #and results[i][1] < 2
            return results[i][4]
        
    for i in range (0,len(results)):
        if (results[i][1] < 2 and results[i][3] > 4):
            return results[i][4]
    
    if ((results[0][3] > 1 and results[0][2] > 0.55) or numResults < 2):
        return results[0][4]
    elif ((results[1][0] < 0.5 and results[1][3] > 1 and results[1][2] > 0.55) or numResults < 3):
        return results[1][4]
    elif (results[2][0] < 0.5 and results[2][3] > 1 and results[2][2] > 0.55):
        return results[2][4]
    else:
        return results[0][4]
    
def probableMapPick (inputresults):
    inputresults.sort(key=itemgetter(0))
    results = list(reversed(inputresults))
    numResults = len(results)
    for i in range (0,len(results)):
        if ((results[i][1] - results[i][3]) > 5 and results[i][0] > 0.8 ): #and results[i][1] < 2
            return results[i][4]
    
    if ((results[0][0] > results[0][2] and results[0][1] > 3) or numResults < 2):
        return results[0][4]
    elif ((results[1][0] > results[1][2] and results[1][1] > 3) or numResults < 3):
        return results[1][4]
    elif (results[2][0] > results[2][2] and results[2][1] > 3):
        return results[2][4]
    else:
        matchdiff = 0
        bestMatch = -1
        for i in range (0, len(results)):
            if ((results[i][0] - results[i][2]) > matchdiff and results[i][1] > 3):
                matchdiff = (results[i][0] - results[i][2])
                bestMatch = i
        return results[bestMatch][4]
    return results[0][4]
    
def allProbableMapBans (resultTeam1, resultTeam2, numBans, numPicks):
    
    teamTurn = True
    allBannedMaps = list ()
    allPickedMaps = list ()
    while ((numBans > 0) or (numPicks > 0)):
        if (len(allBannedMaps) < 2 or (len(allBannedMaps) > 1 and numPicks == 0)):
            bannedMap = ''
            if (teamTurn):
#                print ('Team 1 is banning')
                teamTurn = not teamTurn
                bannedMap = probableMapBan(resultTeam1[:])
            else:
#                print ('Team 2 is banning')
                teamTurn = not teamTurn
                bannedMap = probableMapBan(resultTeam2[:])
            for i in range(0,len(resultTeam1)):
                if (resultTeam1[i][4] == bannedMap):
#                    print (bannedMap)
                    resultTeam1.pop(i)
                    resultTeam2.pop(i)
                    allBannedMaps.append(bannedMap)
                    numBans -= 1
                    break
        else:
            pickedMap = ''
            if (teamTurn):
#                print ('Team 1 is picking')
                teamTurn = not teamTurn
                pickedMap = probableMapPick(resultTeam1[:])
            else:
#                print ('Team 2 is picking')
                teamTurn = not teamTurn
                pickedMap = probableMapPick(resultTeam2[:])
            for i in range(0,len(resultTeam1)):
                if (resultTeam1[i][4] == pickedMap):
#                    print (pickedMap)
                    resultTeam1.pop(i)
                    resultTeam2.pop(i)
                    allPickedMaps.append(pickedMap)
                    numPicks -= 1
                    break
    return [allBannedMaps,allPickedMaps]

def predictBansAndPicks (team1, team2, date, daysBackLimit, numBans, numPicks):
    resultsTotalT1 = list ()
    resultsTotalT2 = list ()
    for i in range(0,len(mapIDs)):
        resultTeam1 = getWinLoseRatioMap(team1,mapIDs[i], date, daysBackLimit)
        resultTeam1Ratio = '{0:.2f}'.format(resultTeam1[0])
        resultTeam1Base = resultTeam1[1]
        resultTeam2 = getWinLoseRatioMap(team2,mapIDs[i], date, daysBackLimit)
        resultTeam2Ratio = '{0:.2f}'.format(resultTeam2[0])
        resultTeam2Base = resultTeam2[1]
        if (resultTeam1Base > 0 or resultTeam2Base > 0):
            resultsTotalT1.append(
                [resultTeam1[0],resultTeam1Base,
                 resultTeam2[0],resultTeam2Base,
                 mapIDs[i]])
            resultsTotalT2.append(
                [resultTeam2[0],resultTeam2Base,
                 resultTeam1[0],resultTeam1Base,
                 mapIDs[i]])
#            print ('{0} | {1} on {2}: ({3}|{4}) \n {5} | {6} \n'.format(
#                team1,
#                team2,
#                mapIDs[i],
#                resultTeam1Base, resultTeam2Base,
#                resultTeam1Ratio, resultTeam2Ratio))
#    print ("-----------------------------")
    maps = allProbableMapBans(resultsTotalT1,resultsTotalT2, numBans, numPicks)
#    print ('Banned maps: ', maps[0])
#    print ('Picked maps: ', maps[1])
#    print ('\n')
    return maps
    
    
print(predictBansAndPicks('SK', 'Liquid',[2016,7,9], 100, 4,0))

#predictBansAndPicks('SK', 'Liquid',[2016,7,9], 100, 3,2)

