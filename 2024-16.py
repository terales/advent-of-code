import nographs as nog

SIGNS = {
  'start': 'S',
  'end': 'E',
  'wall': '#',
  'empty': '.'
}
NEIGHBOURING_MOVES = {
  0 - 1j,
  1 + 0j,
  0 + 1j,
  -1 + 0j,
}
START_DIRECTION = 1 + 0j
STEP_COST = 1
TURN_COST = 1000

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

def graphSolution(input):
  map, start, end = buildMap(input)

  vertexToId = lambda s: s[0]
  startVertex = tuple([start, START_DIRECTION, 0])
  endVertex = tuple([end])
  visited = set([start])

  traversal = nog.TraversalAStarFlex(
    vertexToId,
    nog.GearDefault(),
    next_edges=None,
    next_labeled_edges=lambda p, t: nextSteps(map, visited, p, t),
    is_tree=True
  )

  lastVertex = traversal.start_from(heuristic=lambda v: v[2],start_vertex=startVertex, build_paths=True).go_to(endVertex)

  return lastVertex[2]

def nextSteps(map, visited, vertex, _):
  position = vertex[0]
  previousCost = vertex[2]
  neighbours = [position + move for move in NEIGHBOURING_MOVES]
  for n in neighbours:
    if map[n] == SIGNS['empty'] and not n in visited:
      nextCost, newDirection = getStepCost(position, n, vertex[1])
      cost = previousCost + nextCost
      visited.add(n)
      yield tuple([n, newDirection, cost]), nextCost

def getStepCost(prevStep, step, currDirection):
  score = 0
  directionDifference = step - prevStep - currDirection
  turnedToHorizontal = currDirection.real == 0 and directionDifference.real != 0
  turnedToVertical = currDirection.imag == 0 and directionDifference.imag != 0
  if turnedToHorizontal or turnedToVertical:
    score += TURN_COST
    currDirection = complex(real=currDirection.imag, imag=currDirection.real)

  score += STEP_COST
  prevStep = step
  return score, currDirection


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

print('SampleOne. Expected: 7036, actual:', graphSolution(sampleOne))
print('SampleTwo. Expected: 11048, actual:', graphSolution(sampleTwo))
print('sampleRedditOne. Expected: 21148, actual:', graphSolution(sampleRedditOne))
print('sampleRedditTwo. Expected: 21110, actual:', graphSolution(sampleRedditTwo))


with open('2024-16-input.txt') as f:
  challengeInput = f.read().strip()

print('First challenge:', graphSolution(challengeInput))
