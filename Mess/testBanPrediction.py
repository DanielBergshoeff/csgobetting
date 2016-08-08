from teamPerformance import getRatios

vetoFile = 'matches_vetoProces.txt'

# import existing teamnames
with open('teamIDs.txt', "r") as text_file:
    teamIDs = text_file.readline().split()
    
# import map IDs
with open('mapIDs.txt', "r") as text_file:
    mapIDs = text_file.readline().split()
    
# import event IDs
with open('eventIDs.txt', "r") as text_file:
    eventIDs = text_file.readline().split()

vetoArray = list()
with open(vetoFile,'r') as text_file:
    for line in text_file:
        vetoArray.append(line.replace(" ","").replace("\n","").split(','))


def BO3compare (originalChoices):
    print ('\n**BO3compare called**')
    date = [int(originalChoices[1]), int(originalChoices[2]), int(originalChoices[3])]
    team1 = originalChoices[4]
    team2 = originalChoices[5]
    maps = originalChoices[6].split(';')
    print ('{0} VS {1} on {2}'.format(team1, team2, date))
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
    
    print (numBan, numPick)
    predictedMaps = getRatios(team1, team2, date, 100, numBan, numPick)
    print (predictedMaps)
    numBan = 0
    numPick = 0
    correctMaps = 0.
    for i in range(0,len(maps)):
        if (maps[i] == 'none'):
            break
        else:
            if (numBan <2 or numPick == 2):
                if (predictedMaps[0][numBan] == maps[i]):
                    correctMaps += 1
                print('Ban {0}    {1} | {2}'.format(i,predictedMaps[0][numBan],maps[i]))
                numBan += 1
            else:
                if (predictedMaps[1][numPick] == maps[i]):
                    correctMaps += 1
                print('Pic {0}    {1} | {2}'.format(i,predictedMaps[1][numPick],maps[i]))
                numPick += 1
    print ('correct map ratio {0}'.format(correctMaps/len(maps)))

# lets compare our results
for i in range(0,len(vetoArray)):
    if (vetoArray[i][0] == 'BO_3'):
        BO3compare (vetoArray[i])