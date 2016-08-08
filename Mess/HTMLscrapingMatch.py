import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import numpy as np
from datetime import date
from lxml import html
import requests

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
    


while(True):
    print ('Please provide new match URL, or type \'quit\' to stop')
    sys.stdout.flush()
    linkToMatchPage = str(input())
    #linkToMatchPage = 'http://www.hltv.org/match/2303362-flipsid3-optic-esl-one-cologne-2016'
    if (linkToMatchPage == 'quit'):
        print ('You have quit successfully')
        checkForDouble()
        break
    # download page
    page = requests.get(linkToMatchPage)
    tree = html.fromstring(page.content)
    
    exportList = list()
    
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
        elif (text.lower() == 'august'):
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
            print ('mate this date is so hipster its not on the calendar')
            
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
    
    
    
    # this will create a list of the extracted text
    BOtext = tree.xpath('//div[@class="hotmatchbox"]/div/text()')[:1][0].replace("\n","").strip()
    allTextforVetos = tree.xpath('//div[@class="hotmatchbox"]/div/div/text()')[:7]
    allTextforDate = tree.xpath('//div/span[@style="font-size:14px;"]/text()')[:1][0].replace("\n","").replace("of","").replace("th","").strip()
    #  event = tree.xpath('//div[@class="covSmallHeadline"]/div/text()')
    allVetos = ['','','','','','']
    for i in range(0,len(allTextforVetos)):
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
        if (BOtext[-1:] == '1'):
            exportList.append('BO_1')
        elif (BOtext[-1:] == '3'):
            exportList.append('BO_3')
        else:
            print ('mate this BO is wacky')
    
    date = allTextforDate.split()
    exportList.append(int(date[2]))
    exportList.append(textDatetoNumDate(date[1]))
    exportList.append(int(date[0]))
    
    exportList.append(getTeamNameFromString(allVetos[0]))
    exportList.append(getTeamNameFromString(allVetos[1]))
    
    for i in range(0, len(allVetos)):
        if (allVetos[i]):
            vetoArray = allVetos[i].split()
            vetoMap = getMapIDName(vetoArray[(len(vetoArray) -1)])
            if (vetoMap in mapIDs):
                exportList.append(vetoMap)
            else:
                print ('Youre not on the list (map)')
                
    while (len(exportList) < 12):
        exportList.append('none')
    
    print (allVetos)
    print (exportList)
    
    def checkForDouble():
    import_data = np.genfromtxt(vetoFile,delimiter = ',', dtype="a", autostrip=True)
    import_bestOf = import_data[:,][:,0]
    import_dates = import_data[:,][:,1:4]
    import_homeTeamName = import_data[:,][:,4]
    import_outTeamName = import_data[:,][:,5]
    import_maps = import_data[:,][:,6]
    print (import_maps[1])
    
    for i in range(0, len(import_bestOf)):
        if(import)
    
    
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
    
