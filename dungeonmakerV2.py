import random as R
import copy

FULL = True
BLANK = False

def checkAB(a, b ):
  #swaps the inputs if a > b
  if a > b:
    b, a = a, b
  return a, b

def dist(a, b):
  #Calculates distance between two tuple pairs
  return ((b[0]-a[0])**2 + (b[1]-a[1])**2)**0.5

# def reconstruct_path(cameFrom, current):
#   totalPath = [current]
#   while current in cameFrom.keys():
#     current = cameFrom[current]
#     totalPath.append(current)
#   #print(totalPath)
#   return totalPath

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

  def checkRoomBounds(self, room, returnValue=False):
    if returnValue == False:
      if room.x1 < 0:
        raise IndexError("Room x1 less than minmum")
      if room.x2 > self.x:
        raise IndexError("Room x2 greater than board max")
      if room.y1 < 0:
        raise IndexError("Room y1 less than minimum")
      if room.y2 > self.y:
        raise IndexError("Room y2 greater than board max")
    if returnValue == True:
      if room.x1 < 0:
        return 'x'
      if room.x2 >= self.x:
        return 'x'
      if room.y1 < 0:
        return 'y'
      if room.y2 >= self.y:
        return 'y'

  def checkBounds(self, cellTuple):
    if 0 <= cellTuple[0] < self.y and 0 <= cellTuple[1] < self.x:
      return True
    else:
      return False

  def checkOverlap(self, room):
    '''Checks if a given room overlaps with the edge of the board or another room'''
    x1, x2 = room.x1,room.x2
    y1, y2 = room.y1, room.y2
    #print(room)
    for x in range((x2-x1)+1):
      for y in range((y2-y1)+1):
        try:
          if self.board[room.y1 + y][room.x1 + x].state:
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
        self.checkRoomBounds(room)
        #print(self.board[room.y1 + y][room.x1 + x].state)
        self.board[room.y1 + y][room.x1 + x].setState(FULL)
        self.board[room.y1+y][room.x1+x].setMember(room.getType())

  def placeDoors(self,byOrientation=True):
    if byOrientation == True:
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
              if self.board[y-1][x].state:
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
              if self.board[y+1][x].state:
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
              if self.board[y][x-1].state and self.board[x][y].state:
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
              if self.board[y][x+1].state:
                #print('makin a door')
                self.board[y][x].setDoor(True)
                self.board[y][x+1].setDoor(True)
                match = True
              else:
                options.remove(y)
            except IndexError:
              continue
    else:
      rooms = []
      rooms.extend(self.chamberList)
      rooms.extend(self.hallList)
#      for room in rooms:
#        print(room)

      for room in rooms:
        #print(room)
        options = [1,2,3,4]
        side = R.choice(options)
        #print(side)
        edges = room.getEdge(side)
        #print(edges)
        #print('-'*20)
        R.shuffle(edges)
        cell = edges[0]

        match = False
        while match == False or len(options) == 0:
          cellObj = self.board[cell[0]][cell[1]]
          if side == 1:
            otherCell = self.board[cell[0] - 1][cell[1]]
            if otherCell.state and self.checkBounds((cell[0] - 1,cell[1])) and not room.inRoom(otherCell):
              cellObj.setDoor(True)
              otherCell.setDoor(True)
              #print('door made')
              match = True
            else:
              #print(edges)
              del edges[0]

          elif side == 2:
            otherCell = self.board[cell[0]][cell[1] + 1]
            if otherCell.state and self.checkBounds((cell[0],cell[1] +1)) and not room.inRoom(otherCell):
              cellObj.setDoor(True)
              otherCell.setDoor(True)
              #print('door made')
              match = True
            else:
              #print(edges)
              del edges[0]

          elif side == 3:
            otherCell = self.board[cell[0] + 1][cell[1]]
            if otherCell.state and self.checkBounds((cell[0] + 1,cell[1])) and not room.inRoom(otherCell):
              cellObj.setDoor(True)
              otherCell.setDoor(True)
              match = True
              #print('door made')
            else:
              #print(edges)
              del edges[0]

          elif side == 4:
            otherCell = self.board[cell[0]][cell[1] - 1]
            if otherCell.state and self.checkBounds((cell[0],cell[1] - 1)) and not room.inRoom(otherCell):
              cellObj.setDoor(True)
              otherCell.setDoor(True)
              match = True
              #print('door made')
            else:
              #print(edges)
              del edges[0]

          if len(edges) > 0:
            cell = edges[0]
          else:
            options.remove(side)
            if len(options) > 0:
              side = R.choice(options)
              #print(side)
              edges = room.getEdge(side)
              #print(edges)
              R.shuffle(edges)
              cell = edges[0]




  def hallwayPather(self, start, finish):
    '''Using A* search find the shortest path for the hallway
       start and finish are cell objects'''

    def reconstruct_path(cameFrom, current):
      totalPath = [current]
      while current in cameFrom.keys():
        current = cameFrom[current]
        totalPath.append(current)
      # print(totalPath)
      return totalPath

    #print(start, finish)
    closedSet = set()
    openSet = set()
    openSet.add((start.yLoc,start.xLoc))

    gScore = {(y,x):'i' for x in range(self.x) for y in range(self.y)}
    gScore[(start.yLoc,start.xLoc)] = 0

    fScore = {(y,x):1000000 for x in range(self.x) for y in range(self.y)}
    fScore[(start.yLoc, start.xLoc)] = dist((start.yLoc, start.xLoc),(finish.yLoc, finish.xLoc))
    cameFrom = {}
    count = 0
    while len(openSet) != 0:
      currentMin = 1000000
      for elem in openSet:
        if fScore[elem] < currentMin:
          currentMin = fScore[elem]
          current = elem

      if self.board[current[0]][current[1]] == finish:
        #print(finish, '\n', current)
        #print(reconstruct_path(cameFrom, current))
        return reconstruct_path(cameFrom, current)

      openSet.discard(current)
      closedSet.add(current)

      adjacents = [(current[0],current[1] - 1), (current[0], current[1] + 1),
                    (current[0]-1, current[1]),(current[0]+ 1, current[1])]
      for neighbor in adjacents:
        if 0 <= neighbor[0] < self.y and 0 <= neighbor[1] < self.x:

          if self.board[neighbor[0]][neighbor[1]].state:
            continue
          if neighbor in closedSet:
            continue
          tentative_gScore = gScore[current] + dist(current, neighbor)
          if neighbor not in openSet:
            openSet.add(neighbor)
          elif tentative_gScore >= gScore[neighbor]:
            continue

          cameFrom[neighbor] = current
          gScore[neighbor] = tentative_gScore
          fScore[neighbor] = gScore[neighbor] + dist(neighbor, (finish.yLoc, finish.xLoc))

    raise ValueError("No path exists")

    '''print('closedSet\n',closedSet)
    print('-'*50)
    print('openSet\n',openSet)
    print('\ngScore')
    print('-'*50)
    for k, v in gScore.items():
      print(k, v)
    print('\nfScore')
    print('-'*50)
    for k, v in fScore.items():
      print(k, v)
    print('\ncameFrom')
    print('-'*50)
    for k, v in cameFrom.items():
      print(k, v)'''

  def addHallway(self, hallway):
    if len(self.hallList) > 1:
      options = self.hallList[:]
      start = options.pop()
      while len(options) != 0:
        startTuple = R.choice(start.getOrientSide())
        startCell = self.board[startTuple[0]][startTuple[1]]
        #print(startCell)
        finishTuple = R.choice(options[0].getOrientSide())
        finishCell = self.board[finishTuple[0]][finishTuple[1]]
        #print(finishCell)
        try:
          path = self.hallwayPather(startCell, finishCell)
          hallway.addSequence(path)
        except ValueError:
          pass
        start = options.pop()

  def establishHallway(self, hallway):
    #print(hallway)
    for elem in hallway.cells.keys():
      cell = self.board[elem[0]][elem[1]]
      #print('Cell\n', cell)
      width = hallway.width
      if not cell.state:
        cell.setState(FULL)
        cell.setMember('test')
    for elem in hallway.cells.keys():
      #print(elem)
      for i in range(0 - width // 2, width // 2 + 1):
        cellPlaced = False
        if hallway.cells[elem] == 'North' or 'South':
          if self.checkBounds((elem[0],elem[1] + i)):
            nextcell = self.board[elem[0]][elem[1] + i]
            if not nextcell.state and not cellPlaced:
              #print('nextcell - North/South Right\n', nextcell)
              nextcell.setState(FULL)
              nextcell.setMember('Hallway')
              cellPlaced = True
          if self.checkBounds((elem[0],elem[1] - i)):
            nextcell = self.board[elem[0]][elem[1] - i]
            if not nextcell.state and not cellPlaced:
              #print('nextcell - North/South Left\n', nextcell)
              nextcell.setState(FULL)
              nextcell.setMember('Hallway')
              cellPlaced = True
          else:
            break # Cells to the left and right are full or out of bounds
        if hallway.cells[elem] == 'West' or 'East':
          if self.checkBounds((elem[0] - i,elem[1])):
            nextcell = self.board[elem[0] - i][elem[1]]
            if not nextcell.state and not cellPlaced:
              #print('nextcell - West/East Top\n', nextcell)
              nextcell.setState(FULL)
              nextcell.setMember('Hallway')
              cellPlaced = True
          if self.checkBounds((elem[0] + i,elem[1])):
            nextcell = self.board[elem[0] + i][elem[1]]
            if not nextcell.state and not cellPlaced:
              #print('nextcell - West/East Bot\n', nextcell)
              nextcell.setState(FULL)
              nextcell.setMember('Hallway')
              cellPlaced = True
          else:
            break # Cells to the top and bottom are full or out of bounds

  def __repr__(self):
    rep = '  '
    for x in range(len(self.board[0])):
      rep += '%3d'%(x)
    rep += '\n'
    for y in range(len(self.board)):
      rep += '%3d'%(y)
      for x in range(len(self.board[y])):
        cell = self.board[y][x]
        if not cell.state:
          rep += ' _ '
        elif cell.door:
          rep += ' D '
        elif cell.member == 'Hall':
          rep += ' H '
        elif cell.member == 'Chamber':
          rep += ' C '
        elif cell.member == 'Hallway':
          rep += ' X '
        elif cell.member == 'test':
          rep += ' T '
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

  def __eq__(self, other):
    if self.xLoc == other.xLoc and self.yLoc == other.yLoc:
      return True
    else:
      return False

  def __ne__(self, other):
    if self.xLoc != other.xLoc or self.yLoc != other.yLoc:
      return True
    else:
      return False

  def setDoor(self, newDoor):
    self.door = newDoor

  def setMember(self, newMember):
    self.member = newMember

  def setState(self, newState):
    self.state = newState

  def distance(self, otherCell):
    # calculates distance between two cells, returns float and accepts a tuple of (y,x) or a cell objectas argument
    if type(otherCell) != type((0,0)):
      cellTup = (otherCell.yLoc, otherCell.xLoc)
    else:
      cellTup = otherCell
    return ((self.yLoc - cellTup[0])**2 + (self.xLoc - cellTup[1])**2)**0.5


  def __repr__(self):
    return "({},{})\nState: {}\nMember: {}\nDoor: {}".format(
    self.yLoc, self.xLoc, self.state, self.member, self.door)

class Room(object):
  ''' Container object referencing cells on a board given top-left y, x  and bottom-right y, x'''
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

  def inRoom(self, cell):
    if type(cell) != type((0,0)):
      cellTup = cell.yLoc, cell.xLoc
    elif type(cell) == type((0,0)):
      cellTup = cell
    else:
      raise ValueError("cell must be a cell object or tuple")
    if self.y1 <= cellTup[0] <= self.y2 and self.x1 <= cellTup[1] <= self.x2:
      return True
    else:
      return False

  def getAllEdges(self):
    # returns the edge cells of a room
    retSequence = set()
    for y in range(self.y2 - self.y1 + 1):
      retSequence.add((self.y1 + y, self.x1)) #Left side
      retSequence.add((self.y1 + y, self.x2)) # Right Side
    for x in range(self.x2 - self.x1 + 1):
      retSequence.add((self.y1, self.x1 + x))
      retSequence.add((self.y2, self.x1 + x))
    return list(retSequence)

  def getEdge(self, edge):
    if edge == 1:
      return [(self.y1, x) for x in range(self.x1, self.x2 + 1)]
    elif edge == 2:
      return [(y, self.x2) for y in range(self.y1, self.y2 + 1)]
    elif edge == 3:
      return [(self.y2, x) for x in range(self.x1, self.x2 + 1)]
    elif edge == 4:
      return [(y, self.x1) for y in range(self.y1, self.y2 + 1)]
    else:
      raise ValueError("edge parameter must be either 1, 2 , 3, 4 or 'North', 'East', 'South', 'West'")

  def getOrientSide(self):
    # returns a sequence of tuple cell locations along the orientation facing side of a room
    orientDict = {'North':[(self.y1 - 1, x) for x in range(self.x1, self.x2 + 1)],
                  'South':[(self.y2 + 1, x) for x in range(self.x1, self.x2 + 1)],
                  'East':[(y, self.x2 + 1) for y in range(self.y1, self.y2 + 1)],
                  'West':[(y, self.x1 - 1) for y in range(self.y1, self.y2 + 1)]
                  }
    return orientDict[self.orientation]

  def __repr__(self):
    return "Points: ({},{}),({},{})\nType: {}\nOrientation: {}".format(
    self.y1, self.x1, self.y2, self.x2, self.type, self. orientation)

class Hallway(object):
  '''Hallway object has a value for width and a dictionary to hold cell tuples as keys
  and their path direction as values'''
  def __init__(self):
    self.width = 3 # Odd value, total width of hallway.
    self.type = "Hallway"
    self.cells = {}

  # def addToCells(self, cellTuple):
  #   self.cells.append(cellTuple)

  def addSequence(self, sequence):
    '''Adds a sequence of cell tuples as the keys to the self.cells dictionary,
    also determines the path direction and stores that as the value'''
    if type(sequence) != type([]):
      raise ValueError("Sequence must be of type list")

    def determineDirection(elem, next):
      if elem[0] == next[0] + 1 and elem[1] == next[1]:
        return 'North'
      if elem[0] == next[0] - 1 and elem[1] == next[1]:
        return 'South'
      if elem[1] == next[1] + 1 and elem[0] == next[0]:
        return 'East'
      if elem[1] == next[1] - 1 and elem[0] == next[0]:
        return 'West'

    next = sequence[1]
    for i, elem in enumerate(sequence):
      direction = determineDirection(elem, next)
      self.cells[elem] = direction
      try:
        next = sequence[i+1]
      except IndexError: # Last element in the sequence
        pass

  def __repr__(self):
    return f"Hallway\nWidth:{self.width}\n{self.cells}"

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
  widthOptions = [w for w in range(3, maxSize + 1, step)]
  heightOptions = [h for h in range(3, maxSize + 1, step)]
  height = 0
  while (len(widthOptions) > 0 and len(heightOptions) > 0) and start[1] + height <= hall.y2:
    width = R.choice(widthOptions)
    height = R.choice(heightOptions)
    newRoom = Room(start[0], start[0] + width - 1, start[1], start[1] + height - 1, 'Chamber', 'West')
    #print(newRoom)
    #input("south")
    if board.checkRoomBounds(newRoom, True) == 'x':
      widthOptions.remove(width)
    if board.checkRoomBounds(newRoom, True) == 'y':
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
  widthOptions = [w for w in range(3, maxSize + 1, step)]
  heightOptions = [h for h in range(3, maxSize + 1, step)]
  width, height = 0, 0
  while (len(widthOptions) > 0 and len(heightOptions) > 0) and start[0] - width >= hall.x1:
    width = R.choice(widthOptions)
    height = R.choice(heightOptions)
    #input("West")
    newRoom = Room(start[0] - width + 1, start[0], start[1], start[1] + height - 1, 'Chamber', 'North')
    # print(newRoom)
    if board.checkRoomBounds(newRoom, True) == 'x':
      widthOptions.remove(width)
    if board.checkRoomBounds(newRoom, True) == 'y':
      heightOptions.remove(height)
    if board.checkOverlap(newRoom):
      try:
        board.establishRoom(newRoom)
        start = (start[0] - width, start[1])
        width, height = 0, 0
      except IndexError:
        continue

def chambersEast(board, hall, start, step, maxSize):
  widthOptions = [w for w in range(3, maxSize + 1, step)]
  heightOptions = [h for h in range(3, maxSize + 1, step)]
  width, height = 0, 0
  while (len(widthOptions) > 0 and len(heightOptions) > 0) and start[0] + width <= hall.x2:
    width = R.choice(widthOptions)
    height = R.choice(heightOptions)
    newRoom = Room(start[0], start[0] + width - 1, start[1], start[1] - height + 1, 'Chamber', 'South')
  # print(newRoom)
    if board.checkRoomBounds(newRoom, True) == 'x':
      widthOptions.remove(width)
    if board.checkRoomBounds(newRoom, True) == 'y':
      heightOptions.remove(height)
    if board.checkOverlap(newRoom):
      try:
        board.establishRoom(newRoom)
        start = (start[0] + width, start[1])
        width, height = 0, 0
        #print(board)
      except IndexError:
        continue

def chambersNorth(board, hall, start, step, maxSize):
  widthOptions = [w for w in range(3, maxSize + 1, step)]
  heightOptions = [h for h in range(3, maxSize + 1, step)]
  width, height = 0, 0
  while (len(widthOptions) > 0 and len(heightOptions) > 0) and start[1] - height >= hall.y1:
    width = R.choice(widthOptions)
    height = R.choice(heightOptions)
    newRoom = Room(start[0] - width + 1, start[0], start[1], start[1] - height + 1, 'Chamber', 'East')
      # print(newRoom)
    if board.checkRoomBounds(newRoom, True) == 'x':
      widthOptions.remove(width)
    if board.checkRoomBounds(newRoom, True) == 'y':
      heightOptions.remove(height)
    if board.checkOverlap(newRoom):
      try:
        board.establishRoom(newRoom)
        start = (start[0], start[1] - height)
        width, height = 0, 0
      except IndexError:
        continue

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
  '''Creates a static Hall and Chamber for testing other functions'''
  x2 = board.x // 2
  x1 = x2 - 10
  y2 = board.y // 2
  y1 = y2 - 10
  hall = Room(x1, x2, y1, y2, 'Hall', 'North')
  board.establishRoom(hall)

  chamber = Room(x2+1,x2+4,y1,y1+4,'Chamber', 'West')
  board.establishRoom(chamber)

def test2Hall(board):
  '''Creates two static Halls for testing other functions'''
  x2 = board.x // 4
  x1 = x2 - 5
  y2 = board.y // 4
  y1 = y2 - 5
  hall = Room(x1,x2, y1, y2, 'Hall', 'East')
  board.establishRoom(hall)

  x2 = board.x // 4 * 3
  x1 = x2 - 5
  y2 = board.y // 4 * 3
  y1 = y2 - 5
  hall2 = Room(x1, x2, y1, y2, 'Hall', 'West')
  board.establishRoom(hall2)

def test3HallAndChamber(board):
  '''creates 3 static halls and chambers around them for testing other functions'''
  x2 = board.x // 2
  x1 = x2 - 8
  y2 = board.y // 5
  y1 = y2 -8

  hall = Room(x1, x2, y1, y2, 'Hall', 'South')
  board.establishRoom(hall)

  x2 = board.x // 5
  x1 = x2 - 8
  y2 = board.y // 5 * 4
  y1 = y2 -8

  hall2 = Room(x1, x2, y1, y2, 'Hall', 'East')
  board.establishRoom(hall2)

  x2 = board.x // 5 * 3
  x1 = x2 + 8
  y2 = board.y // 5 * 3
  y1 = y2 + 8

  hall3 = Room(x1, x2, y1, y2, 'Hall', 'West')
  board.establishRoom(hall3)

  chambersAroundHall(board, hall, 'South')
  chambersAroundHall(board, hall2, 'East')
  chambersAroundHall(board, hall3, 'West')

def dungeonmaker(board):
  '''Main algorithm implementation'''
  #create Halls
  pass


board = Board(50, 50)

hall = hallFactory(board)
board.establishRoom(hall)
chambersAroundHall(board, hall, hall.orientation)

hall2 = hallFactory(board)
board.establishRoom(hall2)
chambersAroundHall(board, hall2, hall2.orientation)

hall3 = hallFactory(board)
board.establishRoom(hall3)
chambersAroundHall(board, hall3, hall3.orientation)

#test3HallAndChamber(board)

corridor = Hallway()

board.addHallway(corridor)
board.establishHallway(corridor)

# path = board.hallwayPather(board.board[0][6],board.board[10][9])
# corridor.addSequence(path)
# board.establishHallway(corridor)


board.placeDoors(byOrientation=False)
print(board)







