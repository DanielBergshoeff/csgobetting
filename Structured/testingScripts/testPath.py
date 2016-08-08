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



print(root)

print(script_dir)