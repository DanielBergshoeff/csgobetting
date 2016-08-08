import numpy as np
from datetime import date
import sys

# INSERT NEEDED INFORMATION HERE

totalFile = 'matchFiles/matchesTotal.txt'

import_dates = list()
import_homeTeamName = list()
import_homeTeamScore = list()
import_outTeamName = list()
import_outTeamScore = list()
import_map = list()
import_event = list()

total_dates = list()
total_homeTeamName = list()
total_homeTeamScore = list()
total_outTeamName = list()
total_outTeamScore = list()
total_map = list()
total_event = list()

# import data from import file
def importData ():
    import_data = np.genfromtxt(fileToImport,delimiter = ',')
    global import_dates
    global import_homeTeamName
    global import_homeTeamScore
    global import_outTeamName
    global import_outTeamScore
    global import_map
    global import_event
    import_dates = import_data[:,][:,0:3].tolist()
    import_homeTeamName = import_data[:,][:,3].tolist()
    import_homeTeamScore = import_data[:,][:,4].tolist()
    import_outTeamName = import_data[:,][:,5].tolist()
    import_outTeamScore = import_data[:,][:,6].tolist()
    import_map = import_data[:,][:,7].tolist()
    import_event = import_data[:,][:,8].tolist()
    
    total_data = np.genfromtxt(totalFile,delimiter = ',')
    global total_dates
    global total_homeTeamName
    global total_homeTeamScore
    global total_outTeamName
    global total_outTeamScore
    global total_map
    global total_event
    total_dates = total_data[:,][:,0:3].tolist()
    total_homeTeamName = total_data[:,][:,3].tolist()
    total_homeTeamScore = total_data[:,][:,4].tolist()
    total_outTeamName = total_data[:,][:,5].tolist()
    total_outTeamScore = total_data[:,][:,6].tolist()
    total_map = total_data[:,][:,7].tolist()
    total_event = total_data[:,][:,8].tolist()


# calculations for time difference
def dateDifference (date1, date2):
    d0 = date(int(date1[0]),int(date1[1]),int(date1[2]))
    d1 = date(int(date2[0]),int(date2[1]), int(date2[2]))
    delta = d1 - d0
    return delta.days # if higher than 0: date2 is latest

def combineData ():
    newDates = list()
    newHomeTeamName = list ()
    newHomeTeamScore = list ()
    newOutTeamName = list ()
    newOutTeamScore = list ()
    newMap = list ()
    newEvent = list ()
    
    global import_dates
    global import_homeTeamName
    global import_homeTeamScore
    global import_outTeamName
    global import_outTeamScore
    global import_map
    global import_event
    
    global total_dates
    global total_homeTeamName
    global total_homeTeamScore
    global total_outTeamName
    global total_outTeamScore
    global total_map
    global total_event
    
    while (import_dates or total_dates): # while one of the arrays still contains data
        if (not import_dates):       # if the imported (team) array is empty
            checkDifference = 1      # go immediately to the main-array
        elif (not total_dates):      # if the main-array is empty
            checkDifference = 0      # go immediately to the imported array
        else:                        # if both still contain data, check which one contains the most recent date
            checkDifference = dateDifference (import_dates[0], total_dates[0])  # dateDifference() gives the difference in days
                                                                                # between the the most recent matches in the files
            
        if (checkDifference > 0):    # append the first match from the total list
            doAppend = True
            if (newDates): 
                for i in range(0,len(newDates)): # check all matches in the new combined array for duplicates
                    if (newDates[i] == total_dates[0]):
                        if (
                            (newHomeTeamName[i] == total_homeTeamName[0] or newOutTeamName[i] == total_homeTeamName[0])
                            and
                            (newHomeTeamName[i] == total_outTeamName[0] or newOutTeamName[i] == total_outTeamName[0])
                            and
                            (newMap[i] == total_map[0])):
                            if ((newHomeTeamScore[i] == total_outTeamScore[0] or newOutTeamScore[i] == total_outTeamScore[0])
                                and
                                (newHomeTeamScore[i] == total_homeTeamScore[0] or newOutTeamScore[i] == total_homeTeamScore[0])):
                                doAppend = False # refuse appending the match if it's a duplicate
            if (doAppend):
                # append match to new combined arrays
                newDates.append(total_dates[0])
                newHomeTeamName.append(total_homeTeamName[0])
                newHomeTeamScore.append(total_homeTeamScore[0])
                newOutTeamName.append(total_outTeamName[0])
                newOutTeamScore.append(total_outTeamScore[0])
                newMap.append(total_map[0])
                newEvent.append(total_event[0])
            # remove match from old array
            total_dates.pop(0)
            total_homeTeamName.pop(0)
            total_homeTeamScore.pop(0)
            total_outTeamName.pop(0)
            total_outTeamScore.pop(0)
            total_map.pop(0)
            total_event.pop(0)
        else:                        # append the first match from the imported (team) list
            doAppend = True
            if (newDates):
                for i in range(0,len(newDates)): # check all matches in the new combined array for duplicates
                    if (newDates[i] == import_dates[0]):
                        if (
                            (newHomeTeamName[i] == import_homeTeamName[0] or newOutTeamName[i] == import_homeTeamName[0])
                            and
                            (newHomeTeamName[i] == import_outTeamName[0] or newOutTeamName[i] == import_outTeamName[0])
                            and
                            (newMap[i] == import_map[0])):
                            if ((newHomeTeamScore[i] == import_outTeamScore[0] or newOutTeamScore[i] == import_outTeamScore[0])
                                and
                                (newHomeTeamScore[i] == import_homeTeamScore[0] or newOutTeamScore[i] == import_homeTeamScore[0])):
                                doAppend = False # refuse appending the match if it's a duplicate
            if (doAppend):
                # append match to new combined arrays
                newDates.append(import_dates[0])
                newHomeTeamName.append(import_homeTeamName[0])
                newHomeTeamScore.append(import_homeTeamScore[0])
                newOutTeamName.append(import_outTeamName[0])
                newOutTeamScore.append(import_outTeamScore[0])
                newMap.append(import_map[0])
                newEvent.append(import_event[0])
            # remove match from old array
            import_dates.pop(0)
            import_homeTeamName.pop(0)
            import_homeTeamScore.pop(0)
            import_outTeamName.pop(0)
            import_outTeamScore.pop(0)
            import_map.pop(0)
            import_event.pop(0)
    return [newDates,newHomeTeamName,newHomeTeamScore,newOutTeamName,newOutTeamScore,newMap,newEvent]

def createNewTotalFile (teamName):
    global fileToImport
    fileToImport = 'matchFiles/matches_'
    fileToImport += teamName
    fileToImport += '.txt'
    
    importData()
    
    combinedDataArray = combineData()
    
    dates = combinedDataArray[0]
    date_year = list()
    date_month = list()
    date_day = list()
    # split date
    for i in range(0,len(dates)):
        date_year.append(dates[i][0])
        date_month.append(dates[i][1])
        date_day.append(dates[i][2])
    homeTeamIds = combinedDataArray[1]
    homeTeamScore = combinedDataArray[2]
    outTeamIds = combinedDataArray[3]
    outTeamScore = combinedDataArray[4]
    playedMapIDs = combinedDataArray[5]
    playedEventIDs = combinedDataArray [6]
    
    with open(totalFile, "w+") as text_file:
            for i in range(0,len(dates)):
                text_file.write("{0},{1},{2}, {3}, {4}, {5}, {6}, {7}, {8} \n".format(
                    int(date_year[i]), str(int(date_month[i])).zfill(2), str(int(date_day[i])).zfill(2),
                    str(int(homeTeamIds[i])).zfill(3),
                    str(int(homeTeamScore[i])).zfill(2),
                    str(int(outTeamIds[i])).zfill(3),
                    str(int(outTeamScore[i])).zfill(2),
                    str(int(playedMapIDs[i])).zfill(2),
                    str(int(playedEventIDs[i])).zfill(2)))

teamList = [
    'Astralis',
    'Cloud9',
    'dignitas',
    'EnVyUs',
    'Epsilon',
    'FaZe',
    'FlipSid3',
    'fnatic',
    'G2',
    'Gambit',
    'GODSENT',
    'Immortals',
    'Liquid',
    'mousesports',
    'NatusVincere',
    'NiP',
    'OpTic',
    'SK',
    'TSM',
    'Virtus.pro'
    ]

for i in range(0,len(teamList)):
    createNewTotalFile (teamList[i])
    print ('{0} is processed, {1} to go'.format(teamList[i],19-i))
    sys.stdout.flush()

print ("DONE")
