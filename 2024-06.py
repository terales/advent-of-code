from collections import namedtuple
from enum import Enum

GUARD = '^'
Action = Enum('Action', 'STEP TURN EXIT')
Direction = Enum('Direction', 'UP RIGHT DOWN LEFT')
Position = namedtuple('Position', ['x', 'y'])
Act = namedtuple('Act', ['action', 'newPosition', 'newDirection'])

def main(input):
  map = [list(line) for line in input.split('\n')]
  visitedMap = [row.copy() for row in map]

  visitedPositions = set()
  startingPosition = getStartingPosition(map)
  _markVisit(visitedMap, startingPosition)
  visitedPositions.add(startingPosition)

  acted = act(map, startingPosition, Direction.UP)
  _markVisit(visitedMap, acted.newPosition)

  while acted.action != Action.EXIT:
    if (acted.action == Action.STEP):
      visitedPositions.add(acted.newPosition)
    acted = act(map, acted.newPosition, acted.newDirection)
    _markVisit(visitedMap, acted.newPosition)

  # use _mapToText(visitedMap) to debug
  return len(visitedPositions)

def getStartingPosition(map):
  for rowIndex, row in enumerate(map):
    for columnIndex, cell in enumerate(row):
      if cell == GUARD:
        return Position(columnIndex, rowIndex)

def act(map, currentPosition, direction):
  newPosition = getNewPosition(currentPosition, direction)

  if (newPosition.x < 0 or newPosition.y < 0):
    return Act(Action.EXIT, None, None)

  try:
    newCell = map[newPosition.y][newPosition.x]
    if newCell in ['.', '^']:
      act = Act(Action.STEP, newPosition, direction)
    else:
      act = Act(Action.TURN, currentPosition, getNewDirection(direction))
  except IndexError:
    act = Act(Action.EXIT, None, None)
  
  # print(newCell if 'newCell' in locals() else None, act)
  return act

def getNewPosition(currentPosition, direction):
  match direction:
    case Direction.UP:
      return Position(currentPosition.x, currentPosition.y - 1)
    case Direction.DOWN:
      return Position(currentPosition.x, currentPosition.y + 1)
    case Direction.LEFT:
      return Position(currentPosition.x - 1, currentPosition.y)
    case Direction.RIGHT:
      return Position(currentPosition.x + 1, currentPosition.y)

def getNewDirection(direction):
  directions = list(Direction)
  currentIndex = directions.index(direction)
  try:
    return directions[currentIndex + 1]
  except IndexError:
    return directions[0]

def _markVisit(map, position):
  if position:
    map[position.y][position.x] = 'X'

def _mapToText(map):
  text = ''
  for row in map:
    for cell in row:
      text += cell
    text += '\n'
  return text.strip()


sample = '''
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''.strip()

print(main(sample))
