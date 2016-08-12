import os
import sys
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

if platform == "darwin":
    # OS X
    vetoFile = root+ 'matchFiles/matches_vetoProces.txt'
elif platform == "win32" or platform == "cygwin":
    # Windows
    vetoFile = root+ 'matchFiles\\matches_vetoProces.txt'
    
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
        
top20onHLTV = list ()
# import top-20 HLTV id's
if platform == "darwin":
    # OS X
    with open(root+ 'idFiles/HLTV_top20Teams.txt', "r") as text_file:
        for line in text_file:
            top20onHLTV.append(line.split(',')[0].replace('\n',''))
elif platform == "win32" or platform == "cygwin":
    with open(root+ 'idFiles\\HLTV_top20Teams.txt', "r") as text_file:
        for line in text_file:
            top20onHLTV.append(line.split(',')[0].replace('\n',''))

def textDatetoNumDate (text):
    if (text.lower() == 'january'):
        return (1)
    elif (text.lower() == 'february'):
        return (2)
    elif (text.lower() == 'march'):
        return (3)
    elif (text.lower() == 'april'):
        return (4)
    elif (text.lower() == 'may'):
        return (5)
    elif (text.lower() == 'june'):
        return (6)
    elif (text.lower() == 'july'):
        return (7)
    elif (text.lower() == 'augu'):
        return (8)
    elif (text.lower() == 'september'):
        return (9)
    elif (text.lower() == 'october'):
        return (10)
    elif (text.lower() == 'november'):
        return (11)
    elif (text.lower() == 'december'):
        return (12)
    else:
        print ('mate this date is so hipster its not on the calendar: {0}'.format(text))
        
def getTeamNameFromString (string):
    arrayFromString = string.split()
    if (len(arrayFromString) < 5):
        return arrayFromString[1]
    else:
        return ''.join(arrayFromString[1:(len(arrayFromString)-2)])

def getMapIDName (string):
    newString = string.lower()
    if (newString == 'cobblestone'):
        newString = 'cbble'
    return newString

def getVetos (link):
    # import existing VetoFile
    vetoFileArray = list()
    with open(vetoFile,'r') as text_file:
        for line in text_file:
            vetoFileArray.append(line.replace(" ","").replace("\n","").split(','))
    # download page
    page_vetoPage = requests.get(link)
    tree_vetoPage = html.fromstring(page_vetoPage.content)
    
    exportList = list()
    
    # this will create a list of the extracted text
    allTextforVetos = tree_vetoPage.xpath('//div[@class="hotmatchbox"]/div/div/text()')[:20]
    vetoMatch = False
    for i in range(0,len(allTextforVetos)):
        if (allTextforVetos[i].replace('\n','').replace(':','') == 'Veto process'):
            vetoMatch = True
            vetoPageType = 1
    if (vetoMatch == False):
        allTextforVetos = tree_vetoPage.xpath('//div[@id="mapformatbox"]/text()[preceding-sibling::br]')[:20]
        for i in range(0,len(allTextforVetos)):
            if (allTextforVetos[i].replace('\n','').replace(':','') == 'Veto process'):
                vetoMatch = True
                vetoPageType = 2

    if (vetoMatch):    
        print ("VetoMatch = {0}, type {1}".format(vetoMatch, vetoPageType))
        sys.stdout.flush()
        if (vetoPageType == 1):
            print ("used type 1")
            sys.stdout.flush()
            BOtext = tree_vetoPage.xpath('//div[@class="hotmatchbox"]/div/text()')[:1][0].replace("\n","").strip()
            allTextforDate = tree_vetoPage.xpath('//div/span[@style="font-size:14px;"]/text()')[:1][0].replace("\n","").replace("of","").replace("st","").replace("nd","").replace("th","").replace("rd","").strip()
        if (vetoPageType == 2):
            print ("used type 2")
            sys.stdout.flush()
            BOtext = tree_vetoPage.xpath('//div[@id="mapformatbox"]/text()')[:1][0].replace("\n","").strip()
            allTextforDate = tree_vetoPage.xpath('//div/span[@style="font-size:14px;"]/text()')[:1][0].replace("\n","").replace("of","").replace("st","").replace("nd","").replace("th","").replace("rd","").strip()
    
        #  event = tree.xpath('//div[@class="covSmallHeadline"]/div/text()')
        allVetos = ['','','','','','']
        for i in range(0,len(allTextforVetos)):
            allTextforVetos[i] = allTextforVetos[i].replace("\n","")
            if (allTextforVetos[i][:1] == '1'):
                allVetos[0] = allTextforVetos[i]
            if (allTextforVetos[i][:1] == '2'):
                allVetos[1] = allTextforVetos[i]
            if (allTextforVetos[i][:1] == '3'):
                allVetos[2] = allTextforVetos[i]
            if (allTextforVetos[i][:1] == '4'):
                allVetos[3] = allTextforVetos[i]
            if (allTextforVetos[i][:1] == '5'):
                allVetos[4] = allTextforVetos[i]
            if (allTextforVetos[i][:1] == '6'):
                allVetos[5] = allTextforVetos[i]
        
        if (BOtext[:4] == 'Best'):
            if (BOtext.replace(' (LAN)','')[-1:] == '1'):
                exportList.append('BO_1')
                BOloaded = True
            elif (BOtext.replace(' (LAN)','')[-1:] == '3'):
                exportList.append('BO_3')
                BOloaded = True
            elif (BOtext.replace(' (LAN)','')[-1:] == '5'):
                exportList.append('BO_5')
                BOloaded = True
            elif (BOtext.replace(' (LAN)','')[-1:] == '7'):
                exportList.append('BO_7')
                BOloaded = True
            else:
                print ('mate this BO is wacky {0}'.format(link))
                
        else:
            print ("BO process went wrong, terminating this match: {0}".format(link))
            BOloaded = False
            
        if (BOloaded):
            date = allTextforDate.split()
            exportList.append(int(date[2]))
            exportList.append(textDatetoNumDate(date[1]))
            exportList.append(int(date[0]))
            
            exportList.append(getTeamNameFromString(allVetos[0]))
            exportList.append(getTeamNameFromString(allVetos[1]))
            
            if (exportList[4] == exportList[5]):
                exportList[5] = getTeamNameFromString(allVetos[2])
            
            for i in range(0, len(allVetos)):
                if (allVetos[i]):
                    vetoArray = allVetos[i].split()
                    vetoMap = getMapIDName(vetoArray[(len(vetoArray) -1)])
                    if (vetoArray[(len(vetoArray) -2)] == 'removed'):
                        action = 'rm'
                    else:
                        action = 'pk'
                    if (vetoMap in mapIDs):
                        exportList.append(getTeamNameFromString(allVetos[i]) + '.' + action + '.' + vetoMap)
         #           else:
         #               print ('Youre not on the list (map)')
                        
            while (len(exportList) < 12):
                exportList.append('none')
                
            doAppend = True
            if (vetoArray):
                for i in range(0,len(vetoFileArray)): # check all matches in the new combined array for duplicates
                    if (int(vetoFileArray[i][1]) == exportList[1] and int(vetoFileArray[i][2]) == exportList[2] and int(vetoFileArray[i][3]) == exportList[3]):
                        if (
                            (vetoFileArray[i][4] == exportList[4])
                            and
                            (vetoFileArray[i][5] == exportList[5])):
                            doAppend = False # refuse appending the match if it's a duplicate
            
            if (doAppend):
                with open (vetoFile, 'a') as file:
                    file.write(
                        "{0}, {1},{2},{3}, {4}, {5}, {6}; {7}; {8}; {9}; {10}; {11} \n".format(
                            exportList[0],
                            exportList[1], str(exportList[2]).zfill(2), str(exportList[3]).zfill(2),
                            exportList[4],
                            exportList[5],
                            exportList[6],
                            exportList[7],
                            exportList[8],
                            exportList[9],
                            exportList[10],
                            exportList[11]
                    ))
    
    
    

linkToMatchPage = "http://www.hltv.org/?pageid=188&statsfilter=2048&offset="
offset = 2900

while (True):
    # download page
    linkWithOffset = linkToMatchPage + str(offset)
    page = requests.get(linkWithOffset)
    tree = html.fromstring(page.content)
    
    # check first date
    firstDate = tree.xpath('//div[@class="covSmallHeadline"]/text()')[5]
    if(firstDate[-2:] != '16' and firstDate[-2:] != '15'):
        break
    
    # get teams
    allText = tree.xpath('//div[@class="covSmallHeadline"]/text()')
    del allText[:5]
    homeTeams = list()
    outTeams = list()
    for i in range(0, len(allText)):
        if (i % 4 == 1):
            homeTeams.append(allText[i].split('(')[0].replace(' ',''))
        if (i % 4 == 2):
            outTeams.append(allText[i].split('(')[0].replace(' ',''))
    
    # get all match-page links
    allLinks = tree.xpath('//a[contains(@href, "matchid=")]/@href')
    
    HLTVbase = 'http://www.hltv.org'
    for i in range(0,len(allLinks)):
        print(offset+i)
        sys.stdout.flush()
        
        if (homeTeams[i] in top20onHLTV or outTeams[i] in top20onHLTV):
            matchLink = HLTVbase + allLinks[i]
            
            # download match page
            page_matchLink = requests.get(matchLink)
            tree_matchLink = html.fromstring(page_matchLink.content)
            
            # get link to veto page
            linkToVeto = HLTVbase + tree_matchLink.xpath('//div[@class="covSmallHeadline"]/a[contains(@href, "match")]/@href')[0]
            getVetos(linkToVeto)
        
    offset += 50
 #   if offset > 0:
 #       break