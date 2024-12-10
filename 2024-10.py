from collections import namedtuple
from copy import deepcopy
from yaml import load, SafeLoader

TRAILHEAD = 0
PLEASANT_SLOPE = 1
MAX_STEPS = 9
Position = namedtuple('Position', 'row column')

def main(input):
  map = []
  for line in input.split('\n'):
    row = []
    for character in line:
      row.append(int(character if character != '.' else '-1'))
    map.append(row)

  potentiallyPleasantTrails = [[trailhead] for trailhead in getStartingPositions(map)]

  for step in range(0, MAX_STEPS):
    newTrails = []
    for trail in potentiallyPleasantTrails:
      if len(trail) < step:
        continue

      nextPleasantSteps = getNextPleasantSteps(map, trail[-1], step)
      if len(nextPleasantSteps) == 0:
        continue

      newTrails += [trail + [step] for step in nextPleasantSteps]

    potentiallyPleasantTrails = newTrails
  
  scores = set([(trail[0], trail[-1]) for trail in potentiallyPleasantTrails])
  return len(scores), len(potentiallyPleasantTrails)

def getStartingPositions(map):
  positions = []
  for rowIndex, row in enumerate(map):
    for columnIndex, cell in enumerate(row):
      if cell == TRAILHEAD:
        positions.append(Position(rowIndex, columnIndex))
  return positions

def getNextPleasantSteps(map, currPosition, currHeight):
  nextHeight = currHeight + PLEASANT_SLOPE

  down = getPositionIfPleasant(map, currPosition.row + 1, currPosition.column, nextHeight)
  top = getPositionIfPleasant(map, currPosition.row - 1, currPosition.column, nextHeight)
  right = getPositionIfPleasant(map, currPosition.row, currPosition.column + 1, nextHeight)
  left = getPositionIfPleasant(map, currPosition.row, currPosition.column - 1, nextHeight)

  return list(filter(None, [down, top, right, left]))

def getPositionIfPleasant(map, row, column, nextHeight):
  if row < 0 or column < 0:
    return None

  try:
    if (nextHeight == map[row][column]):
      return Position(row, column)
  except IndexError:
    return None


with open('2024-10-samples.yaml') as f:
  samples = load(f, Loader=SafeLoader)

for sampleIndex, sample in enumerate(samples):
  actual = main(sample['input'].strip())[0]
  print('Test {isPassing}\nExpected: {expected},\nActual:   {actual}\n'.format(
    isPassing = '🟢' if sample['expected'] == actual else '❌',
    expected = sample['expected'],
    actual = actual
  ))

with open('2024-10-input.txt') as f:
  challengeInput = f.read()

print('Day challenges:', main(challengeInput.strip()))
