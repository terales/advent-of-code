from collections import namedtuple, defaultdict
from math import prod
from termcolor import colored

Robot = namedtuple('Robot', 'p v', defaults=[0j, 0j])
DEBUG = False

def main(input, lobbySize, secondsElapsed):
  robots = buildRobotsMap(input)
  robotsAfter = getRobotPositionsAfter(robots, lobbySize, secondsElapsed)

  middleX = lobbySize.real // 2
  middleY = lobbySize.imag // 2

  robotsInQuadrants = defaultdict(int)
  for position in robotsAfter:
    if position.real == middleX or position.imag == middleY:
      continue

    quadrant = complex(int(position.real > middleX), int(position.imag > middleY))
    robotsInQuadrants[quadrant] += 1

  if DEBUG:
    print('original')
    print(_buildDebugMap(lobbySize, [r.p for r in robots]))
    print()
    print('after', colored(secondsElapsed, 'green'))
    print(_buildDebugMap(lobbySize, robotsAfter, hideMiddles=True))

  return prod(robotsInQuadrants.values())

def buildRobotsMap(text):
  robots = []
  for line in text.split('\n'):
    data = line.split(' ')

    pText = data[0].split('=')[1]
    vText = data[1].split('=')[1]

    robots.append(Robot(
      p=complex(*map(int, pText.split(','))),
      v=complex(*map(int, vText.split(',')))
    ))
  return robots

def getRobotPositionsAfter(robots, lobbySize, secondsElapsed):
  arrivedAtPositions = []
  for robot in robots:
    arrivedAtVirtual = robot.p + robot.v * secondsElapsed

    timesTeleported = complex(
      arrivedAtVirtual.real // lobbySize.real * lobbySize.real,
      arrivedAtVirtual.imag // lobbySize.imag * lobbySize.imag
    )
    positionInLobby = arrivedAtVirtual - timesTeleported
    arrivedAtPositions.append(positionInLobby)
  return arrivedAtPositions

def _buildDebugMap(lobbySize, positions, hideMiddles=False):
  if not DEBUG:
    return ''

  map = ''
  DEBUG_SYMBOLS = 'abcdefghijklmnopqrstuvwxyz'
  rowMiddleIndex = round(lobbySize.imag // 2)
  columnMiddleIndex = round(lobbySize.real // 2)

  for row in range(0, round(lobbySize.imag)):
    for column in range(0, round(lobbySize.real)):
      if hideMiddles and (row == rowMiddleIndex or column == columnMiddleIndex):
        map += ' '
        continue

      cell = complex(column, row)
      cellCount = positions.count(cell)
      if cellCount > 0:
        char = DEBUG_SYMBOLS[positions.index(cell)] if cellCount == 1 else cellCount
        map += colored(char, 'green')
      else:
        map += '.'
    map += '\n'
  return map


sampleLobbySize = 11 + 7j
sampleSecondsElapsed = 100
sampleRobots = '''
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
'''.strip()

teleportSampleSecondsElapsed = 5
teleportSampleRobots = '''
p=2,4 v=2,-3
'''.strip()


print(
  'Teleport sample. Expected: {expected}, actual:'
    .format(
      expected=colored('[(1+3j)]', 'green')
    ),
  colored(
    getRobotPositionsAfter(
      buildRobotsMap(teleportSampleRobots),
      sampleLobbySize,
      teleportSampleSecondsElapsed
    ),
    'green'
  )
)

print('Sample. Expected: {expected}, actual: {actual}'.format(
  expected=colored(12, 'green'),
  actual=colored(main(sampleRobots, sampleLobbySize, 100), 'green')
))


with open('2024-14-input.txt') as f:
  challengeLobbySize = 101 + 103j
  challengeBlinks = 100
  challengeInput = f.read().strip()

print('Fist challenge:', colored(main(challengeInput, challengeLobbySize, 100), 'green'))
