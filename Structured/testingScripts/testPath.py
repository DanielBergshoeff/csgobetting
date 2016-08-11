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

allPlayersHLTV = [
    ['coldzera', 9216] 
]

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
        
    
for l in range(0,len(allPlayersHLTV)):
    linkToPlayerPage = 'http://www.hltv.org/?pageid=175&playerid='
    linkToPlayerPage += str(allPlayersHLTV[l][1])
    
    # download page
    page = requests.get(linkToPlayerPage)
    tree = html.fromstring(page.content)
    
    # this will create a list of the extracted text
    datesAndTeams = tree.xpath('//div[@class="covSmallHeadline"]/a/text()')
    rest = tree.xpath('//div[@class="covSmallHeadline"]//text()')
    
    # create lists
    
    
    print(rest)
            
    