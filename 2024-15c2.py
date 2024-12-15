from termcolor import colored

TOP_DISTANCE_MULTIPLIER = 100
DIRECTIONS = {
  '^':  0 - 1j,
  '>':  1 + 0j,
  'v':  0 + 1j,
  '<': -1 + 0j,
}
HORIZONTAL_STEPS = [DIRECTIONS['>'], DIRECTIONS['<']]
SIGNS = {
  'robot': '@',
  'box': 'O',
  'boxWideLeft': '[',
  'boxWideRight': ']',
  'wall': '#',
  'empty': '.'
}
WIDE_BOX_SIGNS = '[]'

def main(input):
  mapText, movementsText = input.split('\n\n')
  map = buildMap(mapText)
  movements = buildMovements(movementsText)
  updatedMap = move(map, movements)
  return calcBoxCoordinatesSum(updatedMap)

def move(map, movements):
  updatedMap = map.copy()
  robotNow = getRobotPosition(updatedMap)

  for step in movements:
    robotAfter = robotNow + step

    if updatedMap[robotAfter] == SIGNS['wall']:
      continue

    if updatedMap[robotAfter] in WIDE_BOX_SIGNS:
      boxesPushed =  pushBoxes(updatedMap, robotAfter, step)
      if boxesPushed is None:
        continue
      sortedUniqueBoxUpdates = getBoxUpdateOrder(boxesPushed, step)
      for leftSide, rightSide in sortedUniqueBoxUpdates:
          updatedMap[leftSide[0]] = SIGNS['empty']
          updatedMap[leftSide[1]] = SIGNS['boxWideLeft']
          if rightSide[0] != leftSide[1]:
            updatedMap[rightSide[0]] = SIGNS['empty']
          updatedMap[rightSide[1]] = SIGNS['boxWideRight']

    updatedMap[robotNow] = SIGNS['empty']
    updatedMap[robotAfter] = SIGNS['robot']
    robotNow = robotAfter

  return updatedMap

def getRobotPosition(map):
  cellIndex = list(map.values()).index(SIGNS['robot'])
  return list(map.keys())[cellIndex]

def pushBoxes(map, boxPosition, step, boxesVisited = {}):
  leftPosition = boxPosition if map[boxPosition] == SIGNS['boxWideLeft'] else boxPosition - 1
  rightPosition = boxPosition if map[boxPosition] == SIGNS['boxWideRight'] else boxPosition + 1

  if (leftPosition, rightPosition) in boxesVisited:
    return boxesVisited

  newLeftPosition = leftPosition + step
  newRightPosition = rightPosition + step

  boxMovement = (
    (leftPosition, newLeftPosition),
    (rightPosition, newRightPosition)
  )

  newLeftHitsWall = map[newLeftPosition] == SIGNS['wall']
  newRightHitsWall = map[newRightPosition] == SIGNS['wall']
  if newLeftHitsWall or newRightHitsWall:
    return None

  isNewLeftEmpty =  map[newLeftPosition] == SIGNS['empty'] or newLeftPosition == rightPosition
  isNewRightEmpty =  map[newRightPosition] == SIGNS['empty'] or newRightPosition == leftPosition
  if isNewLeftEmpty and isNewRightEmpty:
    return [boxMovement]
  
  isNewLeftPushingBox = not isNewLeftEmpty and map[newLeftPosition] in WIDE_BOX_SIGNS
  isNewRightPushingBox = not isNewRightEmpty and map[newRightPosition] in WIDE_BOX_SIGNS
  if isNewLeftPushingBox or isNewRightPushingBox:
    nextBoxPushedByLeft = pushBoxes(map, newLeftPosition, step) if isNewLeftPushingBox else []
    nextBoxPushedByRight = pushBoxes(map, newRightPosition, step) if isNewRightPushingBox else []
    if nextBoxPushedByLeft is not None and nextBoxPushedByRight is not None:
      return nextBoxPushedByLeft + nextBoxPushedByRight + [boxMovement]

def getBoxUpdateOrder(pushedBoxes, step):
  uniqueBoxes = list(set(pushedBoxes.copy()))
  if step == DIRECTIONS['^']:
    sortBy = lambda boxUpdate: boxUpdate[0][1].imag
    isDescending = False
  elif step == DIRECTIONS['>']:
    sortBy = lambda boxUpdate: boxUpdate[1][1].real
    isDescending = True
  if step == DIRECTIONS['v']:
    sortBy = lambda boxUpdate: boxUpdate[1][1].imag
    isDescending = True
  elif step == DIRECTIONS['<']:
    sortBy = lambda boxUpdate: boxUpdate[0][1].real
    isDescending = False
  return sorted(uniqueBoxes, key=sortBy, reverse=isDescending)


def buildMap(text):
  map = {}
  for rowIndex, row in enumerate(text.split('\n')):
    wideMapOffset = 0
    for columnIndex, cell in enumerate(row):
      position = complex(columnIndex + wideMapOffset, rowIndex)
      if cell == SIGNS.get('wall'):
          map[position] = SIGNS['wall']
          map[position + 1] = SIGNS['wall']
      elif cell == SIGNS.get('box'):
          map[position] = SIGNS['boxWideLeft']
          map[position + 1] = SIGNS['boxWideRight']
      elif cell == SIGNS.get('empty'):
          map[position] = SIGNS['empty']
          map[position + 1] = SIGNS['empty']
      elif cell == SIGNS.get('robot'):
          map[position] = SIGNS['robot']
          map[position + 1] = SIGNS['empty']
      else:
          raise Exception('Unexpected character in map input:', cell)
      wideMapOffset += 1
  return map

def buildMapAsIs(text):
  map = {}
  for rowIndex, row in enumerate(text.split('\n')):
    for columnIndex, cell in enumerate(row):
      position = complex(columnIndex, rowIndex)
      map[position] = cell
  return map
      
def buildMovements(text):
  movements = []
  for step in text.replace('\n', ''):
    movements.append(DIRECTIONS[step])
  return movements

def calcBoxCoordinatesSum(map):
  sum = 0
  for position, cell in map.items():
    if cell != SIGNS['boxWideLeft']:
      continue
    
    sum += position.real + TOP_DISTANCE_MULTIPLIER * position.imag
  return round(sum)

def _parseTestInput(fileName):
  with open(fileName) as f:
    parts = f.read().strip().split('\n\n')

  expectedSum = int(parts[0].split(' ')[1])
  mapText = parts[1].split(':')[1].strip()
  steps = [{
      'movements': [],
      'mapAfter': buildMapAsIs(mapText),
  }]

  for part in parts[2:]:
    state, mapText = part.split(':')
    steps.append({
      'movements': buildMovements(state.split(' ')[1]),
      'mapAfter': buildMapAsIs(mapText.strip()),
    })

  return expectedSum, steps

def _printFailedSumTest(testName, expected, actual):
  print(f"{testName}: sum of all boxes' GPS coordinates")
  print('expected:', colored(expected, 'green'))
  print('actual:  ', colored(actual, 'light_red'), end='\n\n')

def _printFailedStepTest(testName, expectedMap, actualMap, stepsMade):
  print(f"{testName}: step test failed on {stepsMade + 1} step")
  print('expected:', '\n' + colored(_visualizeMap(expectedMap), 'green'))
  print('actual:  ', '\n' + colored(_visualizeMap(actualMap), 'light_red'), end='\n\n')

def _visualizeMap(map):
  if len(map) == 0:
    return 'empty map'

  text = ''
  rows = round(max([p.imag for p in map])) + 1
  columns = round(max([p.real for p in map])) + 1

  for rowIndex in range(0, rows):
    for columnIndex in range(0, columns):
      position = complex(columnIndex, rowIndex)
      text += map[position] if position in map else SIGNS['empty']
    text += '\n'

  return text.strip()

def _runTest(filename, testSum=True):
  expectedSum, steps = _parseTestInput(filename)

  initialMap = steps[0]['mapAfter']

  for stepsMade, step in enumerate(steps[1:]):
    updatedMap = move(initialMap, step['movements'])
    if updatedMap == step['mapAfter']:
      initialMap = updatedMap
    else:
      _printFailedStepTest(filename, step['mapAfter'], updatedMap, stepsMade)
      break
  
  if testSum:
    sum = calcBoxCoordinatesSum(updatedMap)
    if sum != expectedSum:
      _printFailedSumTest(filename, expectedSum, sum)

def _testbuildMap():
  expected = '''
    ##############
    ##......##..##
    ##..........##
    ##....[][]@.##
    ##....[]....##
    ##..........##
    ##############
  '''.strip().replace(' ', '')
  actual = buildMap('''
    #######
    #...#.#
    #.....#
    #..OO@#
    #..O..#
    #.....#
    #######
  '''.strip().replace(' ', ''))
  if _visualizeMap(actual) != expected:
    print('❌ Build map failed')
    print('Expected:')
    print(colored(expected, 'green'))
    print('Actual:')
    print(colored(_visualizeMap(actual), 'red'))


_testbuildMap()
_runTest('2024-15-challenge2-sample-small.txt', True)
_runTest('2024-15-challenge2-sample.txt', True)


with open('2024-15-input.txt') as f:
  challengeInput = f.read().strip()

print('Second challenge:', colored(main(challengeInput), 'green'))
