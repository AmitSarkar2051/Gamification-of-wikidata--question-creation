import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import random
import os
import shutil

#global vars
hnFile="ALL_Hindi_proplist_v2.txt"
enFile="ALL_English_proplist_v2.txt"
mapFile='map_proplist.txt'

def create_PropMapFile(myList):
    print("Writing in the  MAP file")
    print("Available size", len(myList))
    with open(mapFile, 'w') as f:
        for item in myList:
            f.write("%s\n" % item)

fhn = open(hnFile, 'r')
fen = open(enFile, 'r')

hnlines = [line for line in fhn.readlines()]
enlines = [line for line in fen.readlines()]
maplines=[]

for i in range(len(hnlines)):
    hnlabel=hnlines[i].strip().strip('\n')
    enlabel=enlines[i].strip().strip('\n')
    if(hnlabel[0] == 'P'):
        maplines.append(hnlabel+","+enlabel)
        #print(hnlabel+","+enlabel)

create_PropMapFile(maplines)
print("Map file created successfully. Please Check: ",mapFile)



