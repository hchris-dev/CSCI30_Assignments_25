class Flag:
  """Flag objects have a country name, a number of colors, a value for each color,
      and an optional imageLink
  Attributes
  ---------------
  name : string
        A country's name
  colorNum : int
        The number of color's in a country's flag
  red - orange : int
        Integer indicating a color's presence
        1 if it is on the flag, 0 if it is not
  imageLink: None, string
        None if there is no link, or if stored in separate csv as in this project
        string with file path or url
  """
  def __init__(self, name, colorNum, red, green, blue, yellow, white, black, orange, imageLink=None):
    """This function creates a Flag object with a name, number of colors, and colors
       as well as an optional image link
    Parameters
    ---------------
    name : string
          Country Name
    colorNum : int
          Number of colors
    red - orange : int
          1 if the color is present, 0 otherwise
    imageLink : None, string
          Optional
          File path or url as a string
    """
    self.name = name #country
    self.colorNum = int(colorNum) #how many colors the flag has
    self.red = int(red) #1 if present, 0 if not, as per dataset
    self.green = int(green)
    self.blue = int(blue)
    self.yellow = int(yellow) #gold in dataset, i am naming it yellow
    self.white = int(white)
    self.black = int(black)
    self.orange = int(orange)
    self.imageLink = imageLink #my first csv has broken links, but does lists colors for each flag
                               #second csv has links but no color data, so this class will be for the 1st list color values
                               #they have different numbers of countries, so I would rather filter with color data and then request an image from the second csv
                               #I am making a csv for the scrambled flags, so i am including imageLink when i create it
  def __str__(self):
    return(f"Flag of {self.name}")
  def __repr__(self):
    return(f"{self.name}'s Flag")
  def returnValue(self, colorString):
    if colorString == "red":
      return(self.red)
    elif colorString == "green":
      return(self.green)
    elif colorString == "blue":
      return(self.blue)
    elif colorString == "yellow":
      return(self.yellow)
    elif colorString == "white":
      return(self.white)
    elif colorString == "black":
      return(self.black)
    elif colorString == "orange":
      return(self.orange)