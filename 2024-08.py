from collections import namedtuple, defaultdict
from copy import deepcopy
from itertools import permutations

ANTINODE_DISTANCE_MULTIPLIER = 2
Position = namedtuple('Position', 'row column')

def main(input, verbose=False):
  map = [list(locations) for locations in input.split('\n')]
  rowBoundary = len(map)
  columnBoundary = len(map[0])

  antennas = defaultdict(set)
  for rowIndex, row in enumerate(map):
    for columnIndex, cell in enumerate(row):
      if (cell != '.'):
        position = Position(row=rowIndex, column=columnIndex)
        antennas[cell].add(position)

  antinodes = set()
  for positions in antennas.values():
    for pair in permutations(positions, 2):
      nextAntinode = getNextAntinodePosition(pair, rowBoundary, columnBoundary)
      if nextAntinode:
        antinodes.add(nextAntinode)
        if verbose: _printAntinode(map, pair, nextAntinode)

  return len(antinodes)

def getNextAntinodePosition(pair, rowBoundary, columnBoundary):
  a, b = pair
  antinode = Position(
    row=getNextPointCoordinate(a.row, b.row),
    column=getNextPointCoordinate(a.column, b.column)
  )
  if not 0 <= antinode.row < rowBoundary:
    return None
  if not 0 <= antinode.column < columnBoundary:
    return None
  return antinode

def getNextPointCoordinate(first, second):
  '''Found formula at https://math.stackexchange.com/a/2109383'''
  return first - ANTINODE_DISTANCE_MULTIPLIER * (first - second)

def _printAntinode(map, pair, antinode):
  markedMap = deepcopy(map)
  for antenna in pair:
    markedMap[antenna.row][antenna.column] = '■'

  try:
    markedMap[antinode.row][antinode.column] = '#'
  except IndexError:
    pass
  
  print('Pair', pair)
  print('Antinode', list(antinode))
  print('\n'.join([''.join(row)for row in markedMap]))
  print()


sample = '''
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''.strip()


print(main(sample))
