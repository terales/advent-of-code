from collections import namedtuple
from copy import deepcopy
from enum import Enum
from tqdm import tqdm

GUARD = '^'
Action = Enum('Action', 'STEP TURN EXIT')
Direction = Enum('Direction', 'UP RIGHT DOWN LEFT')
Position = namedtuple('Position', ['x', 'y'])
Act = namedtuple('Act', ['action', 'newPosition', 'newDirection'])
INFINITE_LOOP_THRESHOLD = 1

class InfiniteLoopException(Exception):
    pass

def main(input):
  map, maxPossiblePositions = parseInput(input)
  startingPosition = getStartingPosition(map)
  visitedPositions = getVisitedPositions(map, startingPosition, maxPossiblePositions)
  return len(visitedPositions)

def getPositionsToEntrapGuard(input):
  map, maxPossiblePositions = parseInput(input)

  trapPositions = set()
  startingPosition = getStartingPosition(map)
  visitedPositions = getVisitedPositions(map, startingPosition, maxPossiblePositions)
  visitedPositions.remove(getStartingPosition(map))
  
  for position in tqdm(visitedPositions):
    obstructedMap = deepcopy(map)
    obstructedMap[position.y][position.x] = 'O'
    try:
      getVisitedPositions(obstructedMap, startingPosition, maxPossiblePositions)
    except InfiniteLoopException:
      trapPositions.add(position)

  return len(trapPositions)

def getVisitedPositions(map, startingPosition, maxPossiblePositions):
  visitedPositions = set()
  visitedPositions.add(startingPosition)

  acted = act(map, startingPosition, Direction.UP)
  stepsMade = 0

  while acted.action != Action.EXIT:
    if (acted.action == Action.STEP):
      visitedPositions.add(acted.newPosition)
    acted = act(map, acted.newPosition, acted.newDirection)

    stepsMade += 1
    if stepsMade > maxPossiblePositions * INFINITE_LOOP_THRESHOLD:
      raise InfiniteLoopException(f'Steps made are {INFINITE_LOOP_THRESHOLD} times bigger that possible positions')

  return visitedPositions

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
  match direction:
    case Direction.UP:
      return Direction.RIGHT
    case Direction.RIGHT:
      return Direction.DOWN
    case Direction.DOWN:
      return Direction.LEFT
    case Direction.LEFT:
      return Direction.UP

def parseInput(text):
  map = [list(line) for line in text.split('\n')]
  maxPossiblePositions = text.count('.')
  return map, maxPossiblePositions

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

with open('2024-06-input.txt') as f:
    challengeInput = f.read()

print(main(sample))
print(main(challengeInput))
print(getPositionsToEntrapGuard(sample))
print(getPositionsToEntrapGuard(challengeInput))
