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
  antinodesAllResonantHarmonics = set()
  for positions in antennas.values():
    for pair in permutations(positions, 2):
      nextAntinode = getNextAntinodePosition(pair, ANTINODE_DISTANCE_MULTIPLIER, rowBoundary, columnBoundary)
      if nextAntinode is None:
        continue
      antinodes.add(nextAntinode)
      antinodesAllResonantHarmonics.add(nextAntinode)

      resonantHarmonicsAntinodes = getResonantHarmonicsAntinodes(pair, rowBoundary, columnBoundary)
      antinodesAllResonantHarmonics.update(resonantHarmonicsAntinodes)
      if verbose:
        _printAntinode(map, pair, nextAntinode)
        [_printAntinode(map, pair, antinode) for antinode in list(resonantHarmonicsAntinodes)]

  for positions in antennas.values():
    if len(positions) > 1:
      antinodesAllResonantHarmonics.update(positions)

  return {
    'Two antinode per pair: ': len(antinodes),
    'Antinodes accounting for resonant harmonics': len(antinodesAllResonantHarmonics)
  }

def getNextAntinodePosition(pair, distance, rowBoundary, columnBoundary):
  a, b = pair
  antinode = Position(
    row=getNextPointCoordinate(a.row, b.row, distance),
    column=getNextPointCoordinate(a.column, b.column, distance)
  )
  if not 0 <= antinode.row < rowBoundary:
    return None
  if not 0 <= antinode.column < columnBoundary:
    return None
  return antinode

def getNextPointCoordinate(first, second, distance):
  '''Found formula at https://math.stackexchange.com/a/2109383'''
  return first - distance * (first - second)

def getResonantHarmonicsAntinodes(pair, rowBoundary, columnBoundary):
  antinodes = set()
  distanceIncrement = ANTINODE_DISTANCE_MULTIPLIER + 1
  while True:
    nextAntinode = getNextAntinodePosition(pair, distanceIncrement, rowBoundary, columnBoundary)
    if nextAntinode is None:
      break
    antinodes.add(nextAntinode)
    distanceIncrement += 1
  return antinodes

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

with open('2024-08-input.txt') as f:
    challengeInput = f.read()

sampleResonantHarmonics = '''
T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........
'''.strip()

print(main(sample))
print(main(challengeInput))
print(main(sampleResonantHarmonics))
