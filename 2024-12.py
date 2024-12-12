from collections import namedtuple
from yaml import load, SafeLoader

Region = namedtuple('Region', 'plant positions')
NUM_OF_SINGLE_PLOT_BORDERS = 4

def main(input):
  garden = {}
  for rowIndex, row in enumerate(input.split('\n')):
    for columntIndex, cell in enumerate(row):
      garden[complex(columntIndex, rowIndex)] = cell

  regions = []
  while(len(garden) > 0):
    firstPosition, firstPlant = getFirstPlot(garden)

    region = Region(
      plant=firstPlant,
      positions=getRegion(firstPosition, firstPlant, garden, set())
    )
    regions.append(region)

    for attributedPosition in region.positions:
      garden.pop(attributedPosition, None)

  totalFencePrice = 0
  for region in regions:
    area = len(region.positions)
    perimeter = calcPerimeter(region)
    totalFencePrice += area * perimeter
  return totalFencePrice

def getRegion(currentPosition, currentPlant, garden, regionPositions):
  regionPositions.add(currentPosition) 
  neighbors = getNeighboringPositions(currentPosition, garden)

  for neighboringPosition in neighbors:
    samePlant = currentPlant == garden.get(neighboringPosition, '')
    alreadyInRegion = neighboringPosition in regionPositions
    if samePlant and not alreadyInRegion:
      regionPositions.update(getRegion(neighboringPosition, currentPlant, garden, regionPositions))

  return regionPositions

def calcPerimeter(region):
  totalPlotBorders = len(region.positions) * NUM_OF_SINGLE_PLOT_BORDERS
  totalAdjustementBorders = sum(len(getNeighboringPositions(position, region.positions)) for position in region.positions)
  return totalPlotBorders - totalAdjustementBorders

def getNeighboringPositions(position, area):
  if len(area) == 0:
    return set()

  neighbors = {
    position + 1,
    position - 1,
    position + 1j,
    position - 1j,
  }

  return set.intersection(neighbors, area)

def getFirstPlot(garden):
  for position, plant in garden.items():
    return position, plant


def _test(test, actual):
  isPassing = test['expected'] == actual
  testData = 'Expected: {expected},\nActual:   {actual}\n'.format(
    expected = test['expected'],
    actual = actual
  )
  return 'Test {isPassing}\n{testData}'.format(
    input = test['input'],
    isPassing = '🟢' if isPassing else '❌',
    testData = testData if not isPassing else ''
  )

with open('2024-12-samples.yaml') as f:
  samples = load(f, Loader=SafeLoader)

for test in samples:
  actual = main(test['input'].strip())
  print(_test(test, actual))


with open('2024-12-input.txt') as f:
  challengeInput = f.read().strip()

print('First challenge:', main(challengeInput))
