from math import inf

SIGNS = {
  'start': 'S',
  'end': 'E',
  'wall': '#',
  'empty': '.'
}
NEIGHBOURING_POSITIONS = {
  0 - 1j,
  1 + 0j,
  0 + 1j,
  -1 + 0j,
}
STEP_COST = 1
TURN_COST = 1000

def main(input):
  map, start, end = buildMap(input)
  
  minimumScore = inf
  paths = []
  paths.append(tuple([start]))

  while len(paths) > 0:
    paths = sorted(paths, key=lambda p: calcPathCost(p) / len(paths), reverse=True)
    path = paths.pop()
    walkableNeighbours = getNewEmptyNeighbours(map, path[-1], path)

    if len(walkableNeighbours) > 0:
      for neighbour in walkableNeighbours:
        paths.append(path + tuple([neighbour]))

    if path[-1] == end:
      pathPrice = calcPathCost(path)
      minimumScore = pathPrice if pathPrice < minimumScore else minimumScore

  return minimumScore

def buildMap(text):
  map = {}
  start = 0j
  end = 0j
  for rowIndex, row in enumerate(text.split('\n')):
    for columnIndex, cell in enumerate(row):
      position = complex(columnIndex, rowIndex)
      cellOnMap = cell

      if cellOnMap == SIGNS['start']:
        start = position
        cellOnMap = SIGNS['empty']
      elif cellOnMap == SIGNS['end']:
        end = position
        cellOnMap = SIGNS['empty']

      map[position] = cellOnMap
  return map, start, end

def getNewEmptyNeighbours(map, p, visited):
  newEmptyNeighbours = set()
  neighbours = [p + n for n in NEIGHBOURING_POSITIONS]
  for n in neighbours:
    if map[n] == SIGNS['empty'] and not n in visited:
      newEmptyNeighbours.add(n)
  return newEmptyNeighbours

def calcPathCost(path):
  score = 0
  currDirection = 1 + 0j
  prevStep = path[0]

  for step in path[1:]:
    directionDifference = step - prevStep - currDirection
    turnedToHorizontal = currDirection.real == 0 and directionDifference.real != 0
    turnedToVertical = currDirection.imag == 0 and directionDifference.imag != 0
    if turnedToHorizontal or turnedToVertical:
      score += TURN_COST
      currDirection = complex(real=currDirection.imag, imag=currDirection.real)

    score += STEP_COST
    prevStep = step

  return score


sampleOne = '''
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
'''.strip()

sampleTwo = '''
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
#'''.strip()

# See https://www.reddit.com/r/adventofcode/comments/1hfhgl1/2024_day_16_part_1_alternate_test_case/
sampleRedditOne = '''
###########################
#######################..E#
######################..#.#
#####################..##.#
####################..###.#
###################..##...#
##################..###.###
#################..####...#
################..#######.#
###############..##.......#
##############..###.#######
#############..####.......#
############..###########.#
###########..##...........#
##########..###.###########
#########..####...........#
########..###############.#
#######..##...............#
######..###.###############
#####..####...............#
####..###################.#
###..##...................#
##..###.###################
#..####...................#
#.#######################.#
#S........................#
###########################
'''.strip()

# See https://www.reddit.com/r/adventofcode/comments/1hfhgl1/comment/m2cbzjl
sampleRedditTwo = '''
########################################################
#.........#.........#.........#.........#.........#...E#
#.........#.........#.........#.........#.........#....#
#....#....#....#....#....#....#....#....#....#....#....#
#....#....#....#....#....#....#....#....#....#....#....#
#....#....#....#....#....#....#....#....#....#....#....#
#....#....#....#....#....#....#....#....#....#....#....#
#....#.........#.........#.........#.........#.........#
#S...#.........#.........#.........#.........#.........#
########################################################
'''.strip()

print('SampleOne. Expected: 7036, actual:', main(sampleOne))
print('SampleTwo. Expected: 11048, actual:', main(sampleTwo))
print('sampleRedditOne. Expected: 21148, actual:', main(sampleRedditOne))
print('sampleRedditTwo. Expected: 21110, actual:', main(sampleRedditTwo))


with open('2024-16-input.txt') as f:
  challengeInput = f.read().strip()

print('First challenge:', main(challengeInput))
