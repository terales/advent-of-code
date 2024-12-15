from termcolor import colored

TOP_DISTANCE_MULTIPLIER = 100
SIGNS = {
  'robot': '@',
  'box': 'O',
  'wall': '#',
  'empty': '.'
}

def main(input):
  mapText, movementsText = input.split('\n\n')
  map = buildMap(mapText)
  movements = buildMovements(movementsText)
  updatedMap = move(map, movements)
  return calcBoxCoordinatesSum(updatedMap)

def move(map, movements):
  initialMap = map.copy()
  updatedMap = {}

  for step in movements:
    robotPosition = list(initialMap.values()).index(SIGNS['robot'])
    positionAfterStep = robotPosition + step
    updatedMap = initialMap

  return updatedMap

def buildMap(text):
  map = {}
  for rowIndex, row in enumerate(text.split('\n')):
    for columnIndex, cell in enumerate(row):
      position = complex(columnIndex, rowIndex)
      map[position] = cell
  return map
      
def buildMovements(text):
  movements = []
  coordinates = {
    '^':  0 - 1j,
    '>':  1 + 0j,
    'v':  0 + 1j,
    '<': -1 + 0j,
  }
  for step in text.replace('\n', ''):
    movements.append(coordinates[step])
  return movements

def calcBoxCoordinatesSum(map):
  sum = 0
  for position, cell in map.items():
    if cell != SIGNS['box']:
      continue
    
    sum += position.real + TOP_DISTANCE_MULTIPLIER * position.imag
  return round(sum)

def _parseTestInput(fileName):
  with open(fileName) as f:
    parts = f.read().strip().split('\n\n')

  expectedSum = parts[0].split(' ')[1]
  mapText = parts[1].split(':')[1].strip()
  steps = [{
      'movements': [],
      'mapAfter': buildMap(mapText),
  }]

  for part in parts[2:]:
    state, mapText = part.split(':')
    steps.append({
      'movements': buildMovements(state.split(' ')[1]),
      'mapAfter': buildMap(mapText.strip()),
    })

  return expectedSum, steps

def _printFailedSumTest(testName, expected, actual):
  print(f"{testName}: sum of all boxes' GPS coordinates")
  print('expected:', colored(expected, 'green'))
  print('actual:  ', colored(actual, 'light_red'), end='\n\n')

def _printFailedStepTest(testName, expectedMap, actualMap):
  print(f"{testName}: step test")
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

  return text

def _runTest(filename, testSum=True):
  expectedSum, steps = _parseTestInput(filename)

  initialMap = steps[0]['mapAfter']
  for step in steps[1:]:
    updatedMap = move(initialMap, step['movements'])
    if updatedMap == step['mapAfter']:
      initialMap = updatedMap
    else:
      _printFailedStepTest(filename, step['mapAfter'], updatedMap)
      break
  
  if testSum:
    sum = calcBoxCoordinatesSum(updatedMap)
    if sum != expectedSum:
      _printFailedSumTest(filename, expectedSum, sum)

_runTest('2024-15-sample-small.txt', False)
_runTest('2024-15-sample.txt', False)
