import numpy as np
from PIL import Image
from urllib.request import urlopen
import matplotlib.pyplot as plt
from .functions import hsvArray, colorCounter, colorPercents, percentSimilar, comparisonResults
from .classes import Flag

worldFlags:list = [] #one csv has country names and colors, but pictures are missing/dead links
flagPictures:dict = {} #other csv has only country names and working links

with open ("./data/flags.csv", "rt") as flagList:
  flagList.readline()
  for line in flagList.readlines():
    line = line.split(";")
    worldFlags.append([line[0], line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17]])
    #appending a list of Flag class attributes

with open ("./data/Countries with Flags URL.csv", "rt") as imageList:
  imageList.readline()
  for line in imageList.readlines():
    line = line.split(",")
    line[-1] = line[-1].split("\n")
    flagPictures[line[0]] = line[-1][0];

riddleFlags:list = []

with open ("./data/scrambledFlags.csv", "rt") as imageList:
  for line in imageList.readlines():
    line = line.split(";")
    riddleFlags.append([line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9]])

flagObjects:list = []
for ii in worldFlags:
  flagObjects.append(Flag(ii[0], ii[1], ii[2], ii[3], ii[4], ii[5], ii[6], ii[7], ii[8]))
  #makes a list of flagObjects using the list of attributes from earlier

riddleObjects:list = []
for ii in riddleFlags:
  riddleObjects.append(Flag(ii[0], ii[1], ii[2], ii[3], ii[4], ii[5], ii[6], ii[7], ii[8], ii[9]))
  #makes a list of flagObjects using the list of scrambled flag attributes from earlier
riddleObjects[0].imageLink = "data/output-flagoffrance.png"
riddleObjects[1].imageLink = "data/output-flagofbrazil.png"
riddleObjects[2].imageLink = "data/output-flagofnamibia.png"
#originally planned to use the three flags from the article, but I had issues with the images
#resorted to recreating the images 

for riddle in riddleObjects:
  comparisonResults(riddle, flagObjects, flagPictures)