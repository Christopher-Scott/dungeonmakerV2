import random as R


FULL = 'Full'
BLANK = 'Blank'


def checkAB(a, b ):
  # swaps the inputs if a > b
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
    self.board = [[] for y in range(self.y)]
    #print(self.board)
    self.getBlankBoard()

  def getBlankBoard(self):
    for y in range(self.y):
      for x in range(self.x):
        newCell = Cell(y,x)
        self.board[y].append(newCell)

  def getMinDimension(self):
    if self.x < self.y:
      return self.x
    return self.y

  def checkOutofBounds(self, room, returnvalue=False):
    if not returnvalue:
      if room.x1 < 0:
        raise IndexError("Room x1 less than minmum")
      if room.x2 > self.x:
        raise IndexError("Room x2 greater than board max")
      if room.y1 < 0:
        raise IndexError("Room y1 less than minimum")
      if room.y2 > self.y:
        raise IndexError("Room y2 greater than board max")
    if returnvalue:
      if room.x1 < 0:
        return 'x'
      if room.x2 > self.x:
        return 'x'
      if room.y1 < 0:
        return 'y'
      if room.y2 > self.y:
        return 'y'

  def checkOverlap(self, room):
    '''Checks if a given room overlaps with the edge of the board or another room'''
    x1, x2 = room.x1,room.x2
    y1, y2 = room.y1, room.y2
    #print(room)
    for x in range((x2-x1)+1):
      for y in range((y2-y1)+1):
        try:
          if self.board[room.y1 + y][room.x1 + x].state == FULL:
            #print('returning false')
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

    #print(room)
    '''investigate whether this runs in (y,x) or (x,y)'''
    for y in range((room.y2 - room.y1) + 1):
      for x in range((room.x2 - room.x1) + 1):
        self.checkOutofBounds(room)
        #print(self.board[room.y1 + y][room.x1 + x].state)
        self.board[room.y1 + y][room.x1 + x].setState(FULL)
        #print(room.y1 + y,room.x1 + x,self.board[room.y1 + y][room.x1 + x].state)
        #print(self.board[room.y1 + y][room.x1 + x].state)
        self.board[room.y1+y][room.x1+x].setMember(room.getType())
        #print(room.y1 + y, room.x1 + x, self.board[room.y1 + y][room.x1 + x].member)
    #print(room)
    #print('room done')

  def placeDoors(self):
    for room in self.chamberList:
      #print(room)
      if room.orientation == 'North':
        match = False
        options = [x for x in range(room.x1, room.x2)]
        #print('north', options)
        while not match and len(options) > 0:
          #print(options)
          x,y = R.choice(options), room.y1
          try:
            #print(self.board[y-1][x])
            #print(self.board[y][x])
            if self.board[y-1][x].state == FULL:
              #print('makin a door')
              self.board[y][x].setDoor(True)
              self.board[y-1][x].setDoor(True)
              match = True
            else:
              options.remove(x)
          except IndexError:
            continue

      elif room.orientation == 'South':
        match = False
        options = [x for x in range(room.x1, room.x2)]
        #print('south', options)
        while not match and len(options) > 0:
          #print(options)
          x, y = R.choice(options), room.y2
          try:
            #print(self.board[y+1][x])
            #print(self.board[y][x])
            if self.board[y+1][x].state == FULL:
              #print('makin a door')
              self.board[y][x].setDoor(True)
              self.board[y+1][x].setDoor(True)
              match = True
            else:
              options.remove(x)
          except IndexError:
            continue

      elif room.orientation == 'West':
        match = False
        options = [y for y in range(room.y1, room.y2+1)]
        #print('west', options)
        while not match and len(options)> 0:
          #print(options)
          x, y = room.x1, R.choice(options)
          try:
            #print(self.board[y][x-1])
            #print(y,x, self.board[y][x])
            if self.board[y][x-1].state == FULL and self.board[x][y].state == FULL:
              #print('makin a door')
              self.board[y][x].setDoor(True)
              self.board[y][x-1].setDoor(True)
              match = True
            else:
              options.remove(y)
          except IndexError:
            continue

      elif room.orientation == 'East':
        match = False
        options = [y for y in range(room.y1, room.y2+1)]
        #print('east', options)
        while not match and len(options) > 0:
          #print(options)
          x, y = room.x2, R.choice(options)
          try:
            #print(self.board[y][x+1])
            #print(self.board[y][x])
            if self.board[y][x+1].state == FULL:
              #print('makin a door')
              self.board[y][x].setDoor(True)
              self.board[y][x+1].setDoor(True)
              match = True
            else:
              options.remove(y)
          except IndexError:
            continue

  def __repr__(self):
    rep = '   '
    for x in range(len(self.board[0])):
      rep += '%3d'%(x)
    rep += '\n'
    for y in range(len(self.board)):
      rep += '%3d'%(y)
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
  def __init__(self, yLocation, xLocation, member=None, state=BLANK):
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

  def __repr__(self):
    return "({},{})\nState: {}\nMember: {}\nDoor: {}".format(
    self.yLoc, self.xLoc, self.state, self.member, self.door)


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
    self.y1, self.x1, self.y2, self.x2, self.type, self. orientation)

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
  height = R.randint(maxSize // 2, maxSize) #arbitrary values for testing'
  orientationList = ['North', 'South', 'East', 'West']
  #print(width, height)
  x2 = R.randint(width, board.x)
  x1 = x2 - width + 1
  y2 = R.randint(height, board.y)
  y1 = y2 - height + 1
  room = Room(x1,x2, y1, y2, 'Hall', R.choice(orientationList))
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
  #finish = False
  #while finish == False:
    #input('south:')
  widthOptions = [w for w in range(3, maxSize + 1, step)]
  heightOptions = [h for h in range(3, maxSize + 1, step)]
  height = 0
  while (len(widthOptions) > 0 and len(heightOptions) > 0) and start[1] + height <= hall.y2:
    width = R.choice(widthOptions)
    height = R.choice(heightOptions)
    newRoom = Room(start[0], start[0] + width - 1, start[1], start[1] + height - 1, 'Chamber', 'West')
    #print(newRoom)
    #input("south")
    if board.checkOutofBounds(newRoom, True) == 'x':
      widthOptions.remove(width)
    if board.checkOutofBounds(newRoom, True) == 'y':
      heightOptions.remove(height)
    if board.checkOverlap(newRoom):
      try:
        board.establishRoom(newRoom)
        start = (start[0], start[1] + height)
        width, height = 0, 0
        #print(board)
      except IndexError:
        continue

      # print(newRoom)
      # print(board)
    #if start[1] + height >= hall.y2:
      #finish = True

def chambersWest(board, hall, start, step, maxSize):
  #finish = False
  #while finish == False:
  widthOptions = [w for w in range(3, maxSize + 1, step)]
  heightOptions = [h for h in range(3, maxSize + 1, step)]
  width, height = 0, 0
  while (len(widthOptions) > 0 and len(heightOptions) > 0) and start[0] - width >= hall.x1:
    width = R.choice(widthOptions)
    height = R.choice(heightOptions)
    #input("West")
    newRoom = Room(start[0] - width + 1, start[0], start[1], start[1] + height - 1, 'Chamber', 'North')
    # print(newRoom)
    if board.checkOutofBounds(newRoom, True) == 'x':
      widthOptions.remove(width)
    if board.checkOutofBounds(newRoom, True) == 'y':
      heightOptions.remove(height)
    if board.checkOverlap(newRoom):
      try:
        board.establishRoom(newRoom)
        start = (start[0] - width, start[1])
        width, height = 0, 0
      except IndexError:
        continue
    #if start[0] - width <= hall.x1:
      # chambers have reached the left edge of the hall, time to change directions
      #finish = True

def chambersEast(board, hall, start, step, maxSize):
  #finish = False
  #while finish == False:
  widthOptions = [w for w in range(3, maxSize + 1, step)]
  heightOptions = [h for h in range(3, maxSize + 1, step)]
  #print(widthOptions)
  #print(heightOptions)
  width, height = 0, 0
  while (len(widthOptions) > 0 and len(heightOptions) > 0) and start[0] + width <= hall.x2:
    width = R.choice(widthOptions)
    height = R.choice(heightOptions)
    #print(width, height)
    #input('east')

    newRoom = Room(start[0], start[0] + width - 1, start[1], start[1] - height + 1, 'Chamber', 'South')
  # print(newRoom)
    if board.checkOutofBounds(newRoom, True) == 'x':
      widthOptions.remove(width)
    if board.checkOutofBounds(newRoom, True) == 'y':
      heightOptions.remove(height)
    if board.checkOverlap(newRoom):
      try:
        board.establishRoom(newRoom)
        start = (start[0] + width, start[1])
        width, height = 0, 0
        #print(board)
      except IndexError:
        continue
    #if start[0] + width >= hall.x2:
      # chambers have reached the right edge of the hall, time to change directions
      #finish = True

def chambersNorth(board, hall, start, step, maxSize):
  #finish = False
  #while finish == False:
  widthOptions = [w for w in range(3, maxSize + 1, step)]
  heightOptions = [h for h in range(3, maxSize + 1, step)]
  width, height = 0, 0
  while (len(widthOptions) > 0 and len(heightOptions) > 0) and start[1] - height >= hall.y1:
    width = R.choice(widthOptions)
    height = R.choice(heightOptions)
    newRoom = Room(start[0] - width + 1, start[0], start[1], start[1] - height + 1, 'Chamber', 'East')
      # print(newRoom)
    if board.checkOutofBounds(newRoom, True) == 'x':
      widthOptions.remove(width)
    if board.checkOutofBounds(newRoom, True) == 'y':
      heightOptions.remove(height)
    if board.checkOverlap(newRoom):
      try:
        board.establishRoom(newRoom)
        start = (start[0], start[1] - height)
        width, height = 0, 0
      except IndexError:
        continue
    #if start[1] - height <= hall.y1:
      # chambers have reached the top edge of the hall, all done
      #finish = True

def chambersAroundHall(board, hall, skip=None):
  '''Places chambers around a hall calling helper functions,
  sides can be skipped by providing an optional list of sides to be skipped'''
  step = 1
  maxSize = board.getMinDimension() // 8 if board.getMinDimension() // 8 >= step else step
  start = (hall.x1 , hall.y1 - 1)

  if 'North' not in skip:
    if hall.y1 > 4:
      # topside
      chambersEast(board, hall, start, step, maxSize)
      #print('topside done')
  start = (hall.x2 + 1, hall.y1)
  #input('proceed')
  if 'East' not in skip:
    if board.x - hall.x2 > 4:
      # right side
      chambersSouth(board, hall, start, step, maxSize)
      #print('right side done')
  start = (hall.x2, hall.y2 + 1)
  #input('proceed')
  if 'South' not in skip:
    if board.y - hall.y2 > 4:
      # bottom side
      chambersWest(board, hall, start, step, maxSize)
      #print('bottom side done')
  start = (hall.x1 - 1, hall.y2)
  #input('proceed')
  if 'West' not in skip:
    if hall.x1 > 4:
      #left side
      chambersNorth(board, hall, start, step, maxSize)
      #print('left side done')

def testHallAndChamber(board):
  x2 = board.x // 2
  x1 = x2 - 10
  y2 = board.y // 2
  y1 = y2 - 10
  hall = Room(x1, x2, y1, y2, 'Hall', 'North')
  board.establishRoom(hall)

  chamber = Room(x2+1,x2+4,y1,y1+4,'Chamber', 'West')
  board.establishRoom(chamber)


def dungeonmaker(board):
  '''Main algorithm implementation'''
  # create Halls
  pass


board = Board(50, 40)
#print(board)
hall = hallFactory(board)
board.establishRoom(hall)
#chambersEast(board,hall,(hall.x1, hall.y1-1), 3, board.getMinDimension()//5)
#chambersSouth(board,hall,(hall.x2 + 1, hall.y1), 3, board.getMinDimension()//5)
chambersAroundHall(board, hall, hall.orientation)
hall2 = hallFactory(board)
board.establishRoom(hall2)
chambersAroundHall(board, hall2, hall2.orientation)
#testHallAndChamber(board)
#print(board)
board.placeDoors()
print(board)
#print(board.hallList)







