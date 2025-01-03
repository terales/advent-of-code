from collections import namedtuple
from copy import deepcopy
from yaml import load, SafeLoader
from termcolor import colored

Region = namedtuple('Region', 'plant positions')
NUM_OF_SINGLE_PLOT_BORDERS = 4
MAX_PLOTS_IN_CROSS = 4

def firstChallenge(input):
  garden = buildGarden(input)
  regions = gatherRegions(garden)
  return getRetailPrice(regions)

def secondChallenge(input):
  garden = buildGarden(input)
  regions = gatherRegions(garden)
  return getBulkPrice(regions)

def buildGarden(text):
  garden = {}
  for rowIndex, row in enumerate(text.split('\n')):
    for columntIndex, cell in enumerate(row):
      garden[complex(columntIndex, rowIndex)] = cell
  return garden

def gatherRegions(originalGarden):
  garden = deepcopy(originalGarden)
  regions = []

  while(len(garden) > 0):
    firstPosition, firstPlant = next(iter(garden.items()))

    positions = extractRegion(firstPosition, firstPlant, garden, set())
    regions.append(Region(firstPlant, positions))

    for attributedPosition in positions:
      garden.pop(attributedPosition, None)

  return regions

def extractRegion(currentPosition, currentPlant, garden, regionPositions):
  regionPositions.add(currentPosition) 
  neighbors = getNeighboringPositions(currentPosition, set(garden))

  for neighboringPosition in neighbors:
    samePlant = currentPlant == garden.get(neighboringPosition, '')
    alreadyInRegion = neighboringPosition in regionPositions
    if samePlant and not alreadyInRegion:
      regionPositions.update(extractRegion(neighboringPosition, currentPlant, garden, regionPositions))

  return regionPositions

def getRetailPrice(regions):
  price = 0
  for region in regions:
    area = len(region.positions)
    perimeter = calcPerimeter(region)
    price += area * perimeter
  return price

def getBulkPrice(regions):
  price = 0
  for region in regions:
    area = len(region.positions)
    sides = countSides(region)
    price += area * sides
  return price

def countSides(region):
  if len(region.positions) == 1:
    return 4

  vertices = 0
  positions = region.positions
  for position in positions:
    topExists = (position - 1j) in positions
    bottomExists = (position + 1j) in positions
    leftExists = (position - 1) in positions
    rightExists = (position + 1) in positions

    topRightExists = (position - 1j + 1) in positions
    topLeftExists = (position - 1j - 1) in positions
    bottomRightExists = (position + 1j + 1) in positions
    bottomLeftExists = (position + 1j - 1) in positions

    numOfNeighbors = len(list(filter(None, [topExists, bottomExists, leftExists, rightExists])))
    numOfDiagonalPlots = len(list(filter(None, [topRightExists, topLeftExists, bottomRightExists, bottomLeftExists])))

    # Definitely an innner plot
    if numOfNeighbors == MAX_PLOTS_IN_CROSS and numOfDiagonalPlots == MAX_PLOTS_IN_CROSS:
      continue

    # Two corners at one plot
    if numOfNeighbors == 1:
      vertices += 2
      continue

    # Could be an exterior corner
    if numOfNeighbors == 2:
      isTopRightCorner = all([leftExists, bottomExists]) and not all([topExists, rightExists]) # ⌝
      isTopLeftCorner = all([rightExists, bottomExists]) and not all([topExists, leftExists])  # ⌜
      isBottomLeftCorner = all([rightExists, topExists]) and not all([bottomExists, leftExists])  # ⌞
      isBottomRightCorner = all([leftExists, topExists]) and not all([bottomExists, rightExists]) # ⌟
      if any([isTopRightCorner, isTopLeftCorner, isBottomLeftCorner, isBottomRightCorner]):
        vertices += 1

    # Check if an interior corner
    if numOfDiagonalPlots < MAX_PLOTS_IN_CROSS:
      looksAtTopRight = all([topExists, rightExists, not topRightExists]) # ⌞
      looksAtTopLeft = all([topExists, leftExists, not topLeftExists])    # ⌟
      looksAtBottomRight = all([bottomExists, rightExists, not bottomRightExists]) # ⌜
      looksAtBottomLeft = all([bottomExists, leftExists, not bottomLeftExists])    # ⌝
      vertices += len(list(filter(None, [looksAtTopRight, looksAtTopLeft, looksAtBottomRight, looksAtBottomLeft])))

  return vertices

def calcPerimeter(region):
  totalPlotBorders = len(region.positions) * NUM_OF_SINGLE_PLOT_BORDERS
  totalAdjustementBorders = sum(len(getNeighboringPositions(position, region.positions)) for position in region.positions)
  return totalPlotBorders - totalAdjustementBorders

def getNeighboringPositions(position, area):
  if len(area) == 0:
    return set()

  return area.intersection({
    position + 1,
    position - 1,
    position + 1j,
    position - 1j,
  })


def _printTest(test, actual):
  isPassing = test['expected'] == actual
  testData = 'Input:\n{input}\nExpected: {expected},\nActual:   {actual}\n'.format(
    input = test['input'],
    expected = test['expected'],
    actual = actual
  )
  message = '{isPassing}{testData}'.format(
    input = test['input'],
    isPassing = '✅' if isPassing else '\n\n❌ ',
    testData = testData if not isPassing else ''
  )
  end = '' if isPassing else '\n'
  print(message, end=end)


with open('2024-12-samples.yaml') as f:
  samples = load(f, Loader=SafeLoader)

print('Retail prices')
for test in samples:
  actual = firstChallenge(test['input'].strip())
  _printTest(test, actual)
print()


with open('2024-12-samples2.yaml') as f:
  samples2 = load(f, Loader=SafeLoader)

print('Sides')
for test in samples2['sides']:
  garden = buildGarden(test['input'].strip())
  regions = gatherRegions(garden)
  sidesCount = sum(countSides(region) for region in regions if region.plant != '.')
  _printTest(test, sidesCount)
print()

print('Bulk prices')
for test in samples2['bulkPrices']:
  actual = secondChallenge(test['input'])
  _printTest(test, actual)
print()


with open('2024-12-input.txt') as f:
  challengeInput = f.read().strip()

print()
print('First challenge:', colored(firstChallenge(challengeInput), 'green'))
print('Second challenge:', colored(secondChallenge(challengeInput), 'green'))
