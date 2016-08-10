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
sys.path.insert(0,root)
from banAndPickPrediction import predictBansAndPicks

vetoFile = root + 'matchFiles/matches_vetoProces.txt'

daysBack = 50
# 50 voor BO3
# 100 voor BO1

# import existing teamnames
with open(root + 'idFiles/teamIDs.txt', "r") as text_file:
    teamIDs = text_file.readline().split()
    
# import map IDs
with open(root + 'idFiles/mapIDs.txt', "r") as text_file:
    mapIDs = text_file.readline().split()
    
# import event IDs
with open(root + 'idFiles/eventIDs.txt', "r") as text_file:
    eventIDs = text_file.readline().split()

vetoArray = list()
with open(vetoFile,'r') as text_file:
    for line in text_file:
        vetoArray.append(line.replace(" ","").replace("\n","").split(','))

numberOfRounds = 0
totalRatio = 0

def BO3compare (originalChoices):
    global numberOfRounds
    global totalRatio
    numberOfRounds += 1
    print(numberOfRounds)
#    print ('\n**BO3compare called**')
    date = [int(originalChoices[1]), int(originalChoices[2]), int(originalChoices[3])]
    team1 = originalChoices[4]
    team2 = originalChoices[5]
    maps = originalChoices[6].split(';')
    banMaps = [maps[0],maps[1],maps[4], maps[5]]
    pickMaps = [maps[2],maps[3]]
#    print ('{0} VS {1} on {2}'.format(team1, team2, date))
    numBan = 0
    numPick = 0
    for i in range(0,len(maps)):
        if (maps[i] == 'none'):
            break
        else:
            if (numBan <2 or numPick == 2):
                numBan += 1
            else:
                numPick += 1
    
#    print (numBan, numPick)
    predictedMaps = predictBansAndPicks(team1, team2, date, daysBack, numBan, numPick)
#    print (predictedMaps)
    numBan = 0
    numPick = 0
    correctMaps = 0.
    for i in range(0,len(maps)):
        if (maps[i] == 'none'):
            break
        else:
            if (numBan <2 or numPick == 2):
                if (predictedMaps[0][numBan] in banMaps):
                    correctMaps += 1
#                print('Ban {0}    {1} | {2}'.format(i,predictedMaps[0][numBan],maps[i]))
                numBan += 1
            else:
                if (predictedMaps[1][numPick] in pickMaps):
                    correctMaps += 1
#                print('Pic {0}    {1} | {2}'.format(i,predictedMaps[1][numPick],maps[i]))
                numPick += 1
#    print ('correct map ratio {0}'.format(correctMaps/(numBan + numPick)))
    totalRatio += (correctMaps/(numBan + numPick))
    
    sys.stdout.flush()

def BO1compare (originalChoices):
    global numberOfRounds
    global totalRatio
    numberOfRounds += 1
    print(numberOfRounds)
#    print ('\n**BO1compare called**')
    date = [int(originalChoices[1]), int(originalChoices[2]), int(originalChoices[3])]
    team1 = originalChoices[4]
    team2 = originalChoices[5]
    maps = originalChoices[6].split(';')
#    print ('{0} VS {1} on {2}'.format(team1, team2, date))
    numBan = 0
    numPick = 0
    for i in range(0,len(maps)):
        if (maps[i] == 'none'):
            break
        else:
            numBan += 1
    
#    print (numBan, numPick)
    predictedMaps = predictBansAndPicks(team1, team2, date, daysBack, numBan, numPick)
#    print (predictedMaps)
    numBan = 0
    numPick = 0
    correctMaps = 0.
    for i in range(0,len(maps)):
        if (maps[i] == 'none'):
            break
        else:
            if (predictedMaps[0][numBan] in maps):
                correctMaps += 1
#            print('Ban {0}    {1} | {2}'.format(i,predictedMaps[0][numBan],maps[i]))
            numBan += 1
#    print ('correct map ratio {0}'.format(correctMaps/numBan))
    totalRatio += (correctMaps/(numBan))
    sys.stdout.flush()
    
# lets compare our results
for i in range(0,len(vetoArray)):
#    if (vetoArray[i][0] == 'BO_3'):
#        BO3compare (vetoArray[i])
    if (vetoArray[i][0] == 'BO_1'):
        BO1compare (vetoArray[i])
        
print('average correctness: {0}'.format(totalRatio/numberOfRounds))
        