import random as R
import time

FULL = 'Full'
BLANK = 'Blank'

def checkAB(a, b ):
  #swaps the inputs if a > b
  if a > b:
    b, a = a, b
  return a, b

class Board(object):
  '''Data structure to hold cells'''
  def __init__(self,xDimension, yDimension):
    self.x = xDimension
    self.y = yDimension
    self.hallList = []
    self.chamberList = []
    self.board = []
    self.getBlankBoard()

  def getBlankBoard(self):
    for y in range(self.y):
      self.board.append([])
      for x in range(self.x):
        newCell = Cell(y,x)
        self.board[y].append(newCell)

  def getMinDimension(self):
    if self.x < self.y:
      return self.x
    return self.y

  def checkOutofBounds(self, room):
    if room.x1 < 0:
      raise IndexError("Room x1 less than minmum")
    if room.x2 > self.x:
      raise IndexError("Room x2 greater than board max")
    if room.y1 < 0:
      raise IndexError("Room y1 less than minimum")
    if room.y2 > self.y:
      raise IndexError("Room y2 greater than board max")

  def checkOverlap(self, room):
    x1, x2 = room.x1,room.x2
    y1, y2 = room.y1, room.y2
    for x in range(x2-x1):
      for y in range(y2-y1):
        try:
          if self.board[room.y1 + y][room.x1 + x].state == FULL:
            return False
        except IndexError:
            return False
    return True

  def establishRoom(self, room):
    '''adds a room to the board and changes the cells to the FULL state'''
    #x1, x2 = checkAB(room.x1, room.x2)
    #y1, y2 = checkAB(room.y1, room.y2)
    #print(x1, y1)
    #print(x2, y2)
    if room.type == 'Hall':
      self.hallList.append(room)
    elif room.type == 'Chamber':
      self.chamberList.append(room)

    for x in range(room.x2 - room.x1):
      for y in range(room.y2 - room.y1):
        self.checkOutofBounds(room)
        self.board[room.y1 + y][room.x1 + x].setState(FULL)
        self.board[room.y1 +y][room.x1 +x].setMember(room.getType())

  # def establishDoors(self):
  #   for room in roomlist:
  #     if room.orientation == 'East':
  #
  #     elif room.orientation == 'West':
  #
  #     elif room.orientation == 'South':
  #
  #     elif room.orientation == 'North':

#Git test comment

  def __repr__(self):
    rep = '   '
    for x in range(len(self.board[0])):
      rep += '%3d'%(x+1)
    rep += '\n'
    for y in range(len(self.board)):
      rep += '%3d'%(y+1)
      for x in range(len(self.board[y])):
        if self.board[y][x].state == BLANK:
          rep += ' _ '
        elif self.board[y][x].door:
          rep += ' D '
        elif self.board[y][x].member == 'Hall':
          rep += ' H '
        elif self.board[y][x].member == 'Chamber':
          rep += ' C '
      rep += '\n'
    return rep

class Cell(object):
  '''Base Data structure'''
  def __init__(self, xLocation, yLocation, member=None, state=BLANK):
    self.xLoc = xLocation
    self.yLoc = yLocation
    self.state = state
    self.member = member
    self.door = False

  def setDoor(self, newDoor):
    self.door = newDoor

  def setMember(self, newMember):
    self.member = newMember

  def setState(self, newState):
    self.state = newState

class Room(object):
  ''' Container object referencing cells on a board given x, y, width, height'''
  def __init__(self, x1, x2, y1, y2, type, orientation='North'):
    x1, x2 = checkAB(x1, x2)
    y1, y2 = checkAB(y1, y2)
    self.x1 = x1
    self.x2 = x2
    self.y1 = y1
    self.y2 = y2
    self.type = type
    self.orientation = orientation

  def setOrientation(self, orientation):
    self.orientation = orientation

  def getWidth(self):
    return self.x2 - self.x1

  def getHeight(self):
    return self.y2 - self.y1

  def getType(self):
    return self.type

  def __repr__(self):
    return "Points: ({},{}),({},{})\nType: {}\nOrientation: {}".format(
    self.x1, self.y1, self.x2, self.y2, self.type, self. orientation)

class Hallway(object):
  def __init__(self):
    self.width = 2
    self.type = "Hallway"
    self.cells = []

  def addToCells(self, cellTuple):
    self.cells.append(cellTuple)

def hallFactory(board):
  # Factory to produce Hall room objects with size restricitons
  maxSize = board.getMinDimension() // 3
  width = R.randint(maxSize // 2,maxSize) #arbitrary values for testing
  height = R.randint(maxSize // 2, maxSize) #arbitrary values for testing
  #print(width, height)
  x2 = R.randint(width ,board.x)
  x1 = x2 - width
  y2 = R.randint(height ,board.y)
  y1 = y2 - height
  room = Room(x1,x2, y1, y2, 'Hall')
  if board.checkOverlap(room):
    return room
  else:
    #print('overlap check fail')
    return hallFactory(board)

def chamberFactory(board):
  # Factory to produce chamber room objects with size restrictions
  maxSize = board.getMinDimension() // 4

  width = R.randint(maxSize // 2,maxSize) #arbitrary values for testing
  height = R.randint(maxSize // 2, maxSize) #arbitrary values for testing
  x2 = R.randint(width, board.x)
  x1 = x2 - width
  y2 = R.randint(height, board.y)
  y1 = y2 - height
  room = Room(x1,x2, y1, y2, 'Chamber')
  if board.checkOverlap(room):
    return room
  else:
    return chamberFactory(board)

def chambersSouth(board, hall, start, step, maxSize):
  finish = False
  while finish == False:
    width = R.randrange(0, maxSize, step)
    height = R.randrange(0, maxSize, step)
    newRoom = Room(start[0], start[0] + width, start[1], start[1] + height, 'Chamber', 'West')
    # print(newRoom)
    if board.checkOverlap(newRoom):
      try:
        board.establishRoom(newRoom)
      except IndexError:
        continue
      # print(newRoom)
      # print(board)
    else:
      #print('checkOverlap fail south')
      continue
    if start[1] + height >= hall.y2:
      finish = True
    else:
      start = (start[0], start[1] + height)

def chambersWest(board, hall, start, step, maxSize):
  finish = False
  while finish == False:
    width = R.randrange(0, maxSize, step)
    height = R.randrange(0, maxSize, step)
    newRoom = Room(start[0] - width, start[0], start[1], start[1] + height, 'Chamber', 'North')
    # print(newRoom)
    if board.checkOverlap(newRoom):
      try:
        board.establishRoom(newRoom)
      except IndexError:
        continue
      # print(newRoom)
      # print(board)
    else:
      #print('checkOverlap fail west')
      continue
    if start[0] - width <= hall.x1:
      # chambers have reached the left edge of the hall, time to change directions
      finish = True
    else:
      start = (start[0] - width, start[1])

def chambersEast(board, hall, start, step, maxSize):
  finish = False
  while finish == False:
    width = R.randrange(0, maxSize, step)
    height = R.randrange(0, maxSize, step)
    newRoom = Room(start[0], start[0] + width, start[1], start[1] - height, 'Chamber', 'South')
    # print(newRoom)
    if board.checkOverlap(newRoom):
      try:
        board.establishRoom(newRoom)
      except IndexError:
        continue
      # print(newRoom)
      # print(board)
    else:
      #print('checkOverlap fail east')
      continue
    if start[0] + width >= hall.x2:
      # chambers have reached the right edge of the hall, time to change directions
      finish = True
    else:
      start = (start[0] + width, start[1])

def chambersNorth(board, hall, start, step, maxSize):
  finish = False
  while finish == False:
    width = R.randrange(0, maxSize, step)
    height = R.randrange(0, maxSize, step)
    newRoom = Room(start[0] - width, start[0], start[1], start[1] - height, 'Chamber', 'East')
    # print(newRoom)
    if board.checkOverlap(newRoom):
      try:
        board.establishRoom(newRoom)
      except IndexError:
        continue
      # print(newRoom)
      # print(board)
    else:
      #print('checkOverlap fail north ')
      continue
    if start[1] - height <= hall.y1:
      # chambers have reached the top edge of the hall, all done
      finish = True
    else:
      start = (start[0], start[1]-height)

def chambersAroundHall(board, hall, skip=None):
  '''Places chambers around a hall calling helper functions,
  sides can be skipped by providing an optional list of sides to be skipped'''
  maxSize = board.getMinDimension() // 5
  start = (hall.x1 , hall.y1)
  step = 3
  print(skip)

  if 'North' not in skip:
    if hall.y1 > 4:
      # topside
      chambersEast(board, hall, start, step, maxSize)
      print('topside done')
  start = (hall.x2, hall.y1)

  if 'East' not in skip:
    if board.x - hall.x2 > 4:
      # right side
      chambersSouth(board, hall, start, step, maxSize)
      print('right side done')
  start = (hall.x2, hall.y2)

  if 'South' not in skip:
    if board.y - hall.y2 > 4:
      # bottom side
      chambersWest(board, hall, start, step, maxSize)
      print('bottom side done')
  start = (hall.x1, hall.y2)


  if 'West' not in skip:
    if hall.x1 > 4:
      #left side
      chambersNorth(board, hall, start, step, maxSize)
      print('left side done')

def dungeonmaker(board):
  '''Main algorithm implementation'''
  #create Halls
  pass


board = Board(50, 40)
#print(board)
hall = hallFactory(board)
board.establishRoom(hall)
#print(hall)
#print(board)
chambersAroundHall(board, hall, hall.orientation)
hall2 = hallFactory(board)
board.establishRoom(hall2)
chambersAroundHall(board, hall2, hall2.orientation)
print(board)






