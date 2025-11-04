import numpy as np
from PIL import Image
from urllib.request import urlopen
import matplotlib.pyplot as plt

def hsvArray(flag, picture, imagePrint=None):
  """This function returns a numpy array of an image's HSV (hue, saturation, value) values.
     flag is the flagObject for the image, and picture is dict of image links

  When imagePrint is set to 1, this function returns an image without converting

  Parameters
  ----------------
  flag : flagObject, string
        This is the key used to get an image's url
        flagObject for HSV array, string for imagePrint
  picture : dict
        A dictionary of names and links to images
  imagePrint : None, int
        Set to 1 to return an image,
        Function returns an HSV array otherwise

  Returns
  ----------------
  np.array
        An array of the image's HSV values
  PIL Image
        The image that corresponds to the flag key
  None
        Returns none if url does not work
  """
  if imagePrint == 1:
    url = picture[flag]
    image = Image.open(urlopen(url))
    return(image)
  try:
    url = picture[flag.name]
    image = Image.open(urlopen(url))
    return(np.asarray(image.convert("HSV")))
  except:
    return(None)
  
def colorCounter(pixelHSVVal):
  """This function returns the color of an inputted pixel.
     It takes in a single pixel, pixelHSVVAL, and returns a string with a color name

  Parameters
  ----------------
  pixelHSVVAL : list
        This is the list of a pixel's HSV values, with 3 ints

  Returns
  ----------------
  string
        The pixel's color
  """
  hue = pixelHSVVal[0]
  saturation = pixelHSVVal[1]
  value = pixelHSVVal[2]


  #hue is a color wheel, where each degree falls within a range of colors
  #PIL has HSV values from 0-255, so hues in if elif statements are converted
  #values were from an article, I tweaked some for pixels that returned none
  if ((saturation < 60) and (value > 180)) == True:
    return('white')
  elif (value < 6) == True:
    return('black')
  elif ((hue < 15) == True) or ((hue > 240) == True):#these values come from multipying the degree for the color by 255/360,
    return('red')                                    #i did it by hand so it doesn't calculate each time, and so i can control the rounding
  elif ((hue > 15) and (hue < 40)) == True:
    return('orange')
  elif ((hue > 40) and (hue < 60)) == True:
    return('yellow')
  elif ((hue > 60) and (hue < 150)) == True:
    return('green')
  elif ((hue > 150) and (hue <240)) == True:
    return('blue')
  else:
    return('white')
  
def colorPercents(flagImageArray):
  """This function returns the percentage of each color in a np.array.
     The array should be made up of lists of 3 ints, HSV values in this project

  Parameters
  ----------------
  flagImageArray : np.array
        This is an array of lists of 3 ints

  Returns
  ----------------
  dict
        color names and their percentage of appearances in the image
  """
  percents = {'red':0, 'green':0, 'orange':0, 'yellow':0, 'blue':0, 'white':0, 'black':0,}
  if flagImageArray is None:
    return(percents)

  counter = 0
  for ii in flagImageArray:
    for jj in range(len(ii)):
      counter += 1
      name = colorCounter(ii[jj])
      percents[name] = percents[name] + 1
  for ii in percents:
    if percents[ii] > 0:
      percents[ii] = percents[ii]/counter

  return(percents)

def percentSimilar(comparison, original):
  """This function returns the similarity between the original
     image's color values, and the comparison image's color values.

  Parameters
  ----------------
  comparison : dict
        A dict of color names and their percentage
        return from colorPercents
  original : dict
        A dict of color names and their percentage

  Returns
  ----------------
  float
        A float rounded to two
        1 minus the percent difference between the images
  """
  compList = []
  origList = []
  counter:int = 0

  for key in original:
    if original[key] == 0:
      pass
    else:
      compList.append(comparison[key])
      origList.append(original[key])
      counter+=1
  temp:int = 0
  for ii in range(counter):
    temp += abs(compList[ii] - origList[ii])

  return(round((1 - (temp/counter))*100, 2))

  #looked online for similarity formula

def comparisonResults(scrambledFlagObject, normalFlagObjectsList, normalFlagImagesDict):
  """This function prints the target flag image, its color percentages, an array of similar flags
     and their images 
     It does not return anything

  Parameters
  ----------------
  scrambledFlagObject : Flag
        A Flag object, can be any flag object with an imageLink in the data folder
  normalFlagObjectsList : list
        A list of flag objects
  normalFlagImagesDict : dict
        A dict of country names and image links
  """
  plt.imshow(Image.open(scrambledFlagObject.imageLink))
  plt.axis('off')
  plt.show() #printing the scrambled image
  
  colorOptions = 7
  colorsList = ["red", "blue", "white", "green", "yellow", "black", "orange"]
  percentRange = 0.1
  
  imageToCompare = Image.open(scrambledFlagObject.imageLink)
  comparisonArray = np.asarray(imageToCompare.convert("HSV"))

  print(f"{scrambledFlagObject.name}: {colorPercents(comparisonArray)}")

  comparisonPercent:dict = colorPercents(comparisonArray) #get percent values for scrambled flag
  similarFlags:dict = {} #dict of similar flags and their similarity

  for flag in normalFlagObjectsList:
    tempMatchCounter = 0
    if flag.colorNum == scrambledFlagObject.colorNum: #check if they have the same number of colors, then check if they have the same colors
      for ii in colorsList:
        if flag.returnValue(ii) == scrambledFlagObject.returnValue(ii):
          tempMatchCounter += 1
      if tempMatchCounter == colorOptions:
        flagPercent = colorPercents(hsvArray(flag, normalFlagImagesDict)) #then calculate percentages
        tempMatchCounter = 0
        for ii in colorsList:
          if (flagPercent[ii] > (comparisonPercent[ii] - percentRange)) and (flagPercent[ii] < (comparisonPercent[ii] + percentRange)):
            tempMatchCounter += 1
        if tempMatchCounter == colorOptions:
          similarFlags[flag.name] = percentSimilar(flagPercent, comparisonPercent)

  sortArray:np.array = np.array(list(similarFlags.items()))
  sortIndices:np.array = np.flip(np.argsort(np.array(list(similarFlags.values()))))
  sortArray:np.array = sortArray[sortIndices]
  print(sortArray)

  for ii in sortArray:
    plt.imshow(hsvArray((str(ii).split("'")[1]), normalFlagImagesDict, imagePrint = 1)) #gets an array item, casts to string, splits, and accesses the country name string
    plt.axis('off')
    plt.show()