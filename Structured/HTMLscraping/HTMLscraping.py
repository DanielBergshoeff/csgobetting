import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

from lxml import html
import requests

# INSERT NEEDED INFORMATION HERE
teamIDsOnHLTV = [
    6665, # Astralis
    5752, # Cloud9
    5422, # dignitas
    5991, # EnVyUs
    4688, # Epsilon
    6667, # FaZe
    5988, # FlipSid3
    4991, # fnatic
    5995, # G2
    6651, # Gambit
    6902, # GODSENT
    7010, # Immortals
    5973, # Liquid
    4494, # mousesports
    4608, # Natus Vincere
    6615, # OpTic
    6137, # SK
    5996, # TSM
    5378, # Virtus.pro
    4411, # NiP
]
#linkToMatchPage = 'http://www.hltv.org/?pageid=188&teamid='

# import existing teamnames
with open('../idFiles/teamIDs.txt', "r") as text_file:
    teamIDs = text_file.readline().split()
    
# import map IDs
with open('../idFiles/mapIDs.txt', "r") as text_file:
    mapIDs = text_file.readline().split()
    
# import event IDs
with open('../idFiles/eventIDs.txt', "r") as text_file:
    eventIDs = text_file.readline().split()


for i in range(0,len(teamIDsOnHLTV)):
    linkToMatchPage = 'http://www.hltv.org/?pageid=188&teamid='
    linkToMatchPage += str(teamIDsOnHLTV[i])
    
    # download page
    page = requests.get(linkToMatchPage)
    tree = html.fromstring(page.content)
    
    # this will create a list of the extracted text
    allText = tree.xpath('//div[@class="covSmallHeadline"]/text()')
    event = tree.xpath('//div[@class="covSmallHeadline"]/div/text()')
    for i in range(0,len(event)): # prepare eventnames in utf-8 standard
        newEvent = event[i].encode("utf-8")
        event[i] = newEvent.replace(" ","_")
    
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
    
    # split and process collected list to individual lists
    for i in range(5,len(allText)):
        currentI = (i-5) % 4
        if (currentI == 0):
            dates.append(allText[i].replace(" ","/20"))
        if (currentI == 1):
            homeTeam.append(allText[i].replace(" ",""))
        if (currentI == 2):
            outTeam.append(allText[i].replace(" ",""))
        if (currentI == 3):
            map.append(allText[i])
    
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
    playedEventIDs = list ()
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
            
    for i in range(0, len(event)):
        if (event[i] in eventIDs):
            playedEventIDs.append(eventIDs.index(event[i]))
        else:
            eventIDs.append(event[i])
            playedEventIDs.append(eventIDs.index(event[i]))
    
    # write everything to file
    teamName = homeTeamName[0]
    teamName += '.txt'
    filename = '../matchFiles/matches_'
    filename += teamName
    with open(filename, "w+") as text_file:
        for i in range(0,len(dates)):
            text_file.write("{0},{1},{2}, {3}, {4}, {5}, {6}, {7}, {8} \n".format(
                date_year[i], str(date_month[i]).zfill(2), str(date_day[i]).zfill(2),
                str(homeTeamIds[i]).zfill(3),
                str(homeTeamScore[i]).zfill(2),
                str(outTeamIds[i]).zfill(3),
                str(outTeamScore[i]).zfill(2),
                str(playedMapIDs[i]).zfill(2),
                str(playedEventIDs[i]).zfill(2)))

# update ID files
with open('../idFiles/eventIDs.txt', 'w+') as text_file:
    for i in range(0,len(eventIDs)):
        text_file.write("{0} ".format(eventIDs[i]))
        
with open('../idFiles/mapIDs.txt', 'w+') as text_file:
    for i in range(0,len(mapIDs)):
        text_file.write("{0} ".format(mapIDs[i]))
        
with open('../idFiles/teamIDs.txt', 'w+') as text_file:
    for i in range(0,len(teamIDs)):
        text_file.write("{0} ".format(teamIDs[i]))


print ("DONE")