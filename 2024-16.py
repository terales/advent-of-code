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

def main(input):
  map, start, end = buildMap(input)
  pathsToEnd = walk(map, end, {tuple([start])})
  # TODO calc price of walking the path
  return 0

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


def walk(map, end, visited):
  newVisited = set()
  for path in visited:
    if path[-1] == end:
      newVisited.add(path)
      continue

    neighbours = getNewEmptyNeighbours(map, path[-1], path)
    if len(neighbours) == 0:
      continue

    for neighbour in neighbours:
      newVisited.add(path + tuple([neighbour]))

  return walk(map, end, newVisited) if visited != newVisited else newVisited

def getNewEmptyNeighbours(map, p, visited):
  newEmptyNeighbours = set()
  neighbours = [p + n for n in NEIGHBOURING_POSITIONS]
  for n in neighbours:
    if map[n] == SIGNS['empty'] and not n in visited:
      newEmptyNeighbours.add(n)
  return newEmptyNeighbours

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


print('SampleOne. Expected: 7036, actual: ', main(sampleOne))
print('SampleTwo. Expected: 11048, actual: ', main(sampleTwo))
