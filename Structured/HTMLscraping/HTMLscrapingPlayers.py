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

# define min and max offset
minoffset = 0
maxoffset = 350


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
        
    
for i in range(minoffset, maxoffset):
    print('Offset = ' + str(i))
#    linkToMatchesPage = 'http://www.hltv.org/?pageid=188&statsfilter=2048&offset='
    linkToMatchesPage = 'http://www.hltv.org/?pageid=188&statsfilter=0&offset='
    linkToMatchesPage += str(i * 50)
    
    linkHLTV = 'http://www.hltv.org'
    
    # download page
    page = requests.get(linkToMatchesPage)
    tree = html.fromstring(page.content)
    
    # this will create a list of the extracted text    
    allLinks = tree.xpath('//a[contains(@href, "matchid=")]/@href')
    
    for l in range(0, len(allLinks)):
        print('Match no. ' + str(l))
        linkToMatch = linkHLTV + allLinks[l]
        emailnr = 0
        newinterface = None
        # download page
        page = requests.get(linkToMatch)
        tree = html.fromstring(page.content)
        
        rest = tree.xpath('//div[@class="covSmallHeadline"]//text()')
        
        homeTeamName = rest[1].replace(" ", "")
        outTeamName = rest[3].replace(" ", "")
        
        dateAndTime = rest[5]
        dateandtime = rest[5].split(" ")
        date = dateandtime[0]
        
        year = date.split("-")[0]
        month = date.split("-")[1]
        day = date.split("-")[2]
        time = dateandtime[1]
        
        map = rest[7]
        event = rest[9]
        homeTeamScore = rest[11]
        outTeamScore = rest[13]
        homeTeamWonRoundsCT = rest[15]
        outTeamWonRoundsT = rest[17]
        homeTeamWonRoundsT = rest[19]
        outTeamWonRoundsCT = rest[21]
        
        if(not homeTeamWonRoundsCT.isdigit() or not outTeamWonRoundsT.isdigit()):
            emailnr -= 3
        
        # fix numeration in case of emails as names
        if str(rest[23]) != 'Team rating':
            emailnr += 2
        if("email" in rest[34 + emailnr]):
            emailnr += 1
        if("damage" not in rest[36 + emailnr]):            
            newinterface = True  
        if("email" in rest[38 + emailnr]):
            emailnr += 1
        if("email" in rest[42 + emailnr]):
            emailnr += 1
        if("email" in rest[46 + emailnr]):
            emailnr += 1
        if("email" in rest[50 + emailnr]):
            emailnr += 1        
        if(not newinterface):
            if("email" in rest[54 + emailnr]):
                emailnr += 1
        else:
            emailnr -= 5
        
        if("Round history" not in rest[56 + emailnr]):
            emailnr -= 1
        
        # convert names to IDs
        if (homeTeamName in teamIDs):
            homeTeamId = teamIDs.index(homeTeamName)
        else:
            teamIDs.append(homeTeamName)
            homeTeamId = teamIDs.index(homeTeamName)
       
        if (outTeamName in teamIDs):
            outTeamId = teamIDs.index(outTeamName)
        else:
            teamIDs.append(outTeamName)
            outTeamId = teamIDs.index(outTeamName)
    
        if (map in mapIDs):
            playedMapID = mapIDs.index(map)
        else:
            mapIDs.append(map)
            playedMapID = mapIDs.index(map)
            
        if (event in eventIDs):
            playedEventID = eventIDs.index(event)
        else:
            eventIDs.append(event)
            playedEventID = eventIDs.index(event)      
            
        for p in range(0, 10):
            
            if(not newinterface):
                x = p * 12
            else:
                x = p * 11
            
            if(len(rest) > (69 + x + emailnr)):    
                playerName = rest[69 + x + emailnr].replace("/", "").replace("*", "").replace("\\", "").replace("\\t", "").replace(" ", "").replace("|", "")
                playerName = ''.join(playerName.split())
                if("email" in playerName):
                    emailnr += 1
                playerName.encode("utf-8")
                playerTeam = rest[70 + x + emailnr].replace(" ", "")
                print(playerTeam)
                playerKills = rest[71 + x + emailnr].replace(" ", "")
                print(playerKills)
                playerDeaths = rest[74 + x + emailnr]
                print(playerDeaths)
            
                if(newinterface):
                    playerRating = rest[78 + x + emailnr]
                else:
                    playerRating = rest[79 + x + emailnr]
                print(playerRating)
                
                # convert names to IDs
                if (playerTeam in teamIDs):
                    playerTeamId = teamIDs.index(playerTeam)
                else:
                    teamIDs.append(playerTeam)
                    playerTeamId = teamIDs.index(playerTeam)
                
                
                # write to file       
                playerNameForFileName = playerName + '.txt'
    
                if platform == "darwin":
                    # OS X
                    filename = root + 'playerMatchFiles/matches_'
                elif platform == "win32" or platform == "cygwin":
                    # Windows
                    filename = root + 'playerMatchFiles\\matches_'
             
                filename += playerNameForFileName
                with open(filename, "a", encoding='utf-8') as text_file:
                    text_file.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17} \n".format(
                    year, month, day, time,
                    homeTeamId, outTeamId,
                    playedMapID, playedEventID,
                    homeTeamScore, outTeamScore,
                    homeTeamWonRoundsCT, outTeamWonRoundsT, homeTeamWonRoundsT, outTeamWonRoundsCT,
                    playerTeamId, playerKills, playerDeaths, playerRating))

# update ID files
if platform == "darwin":
    # OS X
    with open(root+ 'idFiles/eventIDs.txt', 'w+') as text_file:
        for i in range(0,len(eventIDs)):
            text_file.write("{0} ".format(eventIDs[i]))
    with open(root+ 'idFiles/mapIDs.txt', 'w+') as text_file:
        for i in range(0,len(mapIDs)):
            text_file.write("{0} ".format(mapIDs[i]))
    with open(root+ 'idFiles/teamIDs.txt', 'w+') as text_file:
        for i in range(0,len(teamIDs)):
            text_file.write("{0} ".format(teamIDs[i]))
elif platform == "win32" or platform == "cygwin":
    # Windows
    with open(root+ 'idFiles\\eventIDs.txt', 'w+') as text_file:
        for i in range(0,len(eventIDs)):
            text_file.write("{0} ".format(eventIDs[i]))
    with open(root+ 'idFiles\\mapIDs.txt', 'w+') as text_file:
        for i in range(0,len(mapIDs)):
            text_file.write("{0} ".format(mapIDs[i]))
    with open(root+ 'idFiles\\teamIDs.txt', 'w+') as text_file:
        for i in range(0,len(teamIDs)):
            text_file.write("{0} ".format(teamIDs[i]))
        
print('DONE')