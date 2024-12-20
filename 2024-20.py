from collections import Counter
from copy import deepcopy
from math import inf
import networkx as nx

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
WEIGHT_ATTR = 'weight'

def main(input):
  map, start, end = buildMap(input)
  pass

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

def buildGraph(map):
  graph = nx.Graph()

  for position, terrain in map.items():
    graph.add_node(position, terrain=terrain)

    for move in NEIGHBOURING_MOVES:
      destination = position + move
      if destination not in map:
        continue

      graph.add_node(destination, terrain=map[destination])
      graph.add_edge(position, destination, weight=calcEdgeWeight(terrain, map[destination]))

  return graph

def getShortestPath(graph, start, end):
  return nx.shortest_path(graph, source=start, target=end, weight='weight')

def getFastestTime(graph, start, end):
  path = getShortestPath(graph, start, end)
  return round(nx.path_weight(graph, path, weight='weight'))

def calcEdgeWeight(fromTerrain, toTerrain):
  weight = 1
  if SIGNS['wall'] in [fromTerrain, toTerrain]:
    weight = inf
  return weight

def getCheatingOptions(graph, path):
  cheatsTried = set()
  for position in path:
    for neighbor in graph.neighbors(position):
      if neighbor in cheatsTried:
        continue

      if graph.nodes[neighbor].get('terrain', '') != SIGNS['wall']:
        continue
 
      validNextSteps = getValidNextSteps(graph, neighbor, position)
      if len(validNextSteps) == 0:
        continue

      cheatsTried.add(neighbor)
      cheatingOption = deepcopy(graph)
      cheatingOption.nodes[neighbor]['terrain'] = SIGNS['empty']
      for edge in cheatingOption.edges(neighbor):
        if edge[1] == position or edge[1] in validNextSteps:
          cheatingOption.edges[edge]['weight'] = 1
      yield cheatingOption

def getValidNextSteps(graph, currentStep, previousStep):
  steps = []
  for step in graph.neighbors(currentStep):
    if step == previousStep:
      continue
    elif graph.nodes[step].get('terrain', '') == SIGNS['wall']:
      continue
    else:
      steps.append(step)
  return steps


def _visualizeMaze(graph, highlight = []):
  text = ''
  rows = round(max([n.imag for n in graph.nodes])) + 1
  columns = round(max([p.real for p in graph.nodes])) + 1

  for rowIndex in range(0, rows):
    for columnIndex in range(0, columns):
      position = complex(columnIndex, rowIndex)
      if position not in highlight:
        text += graph.nodes[position]['terrain'] if position in graph.nodes else SIGNS['empty']
      else:
        text += '█'
    text += '\n'

  return text

sample = '''
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
'''.strip()


def _testGetFastestTime(input, expected):
  map, start, end = buildMap(input)
  graph = buildGraph(map)
  time = getFastestTime(graph, start, end)
  if time != expected:
    print(f"❌ Fastest time didn't match. Expected: {expected}, actual: {time}")

_testGetFastestTime(sample, 84)


def _testCheats(input, expectations):
  map, start, end = buildMap(input)
  graph = buildGraph(map)
  originalShortestPath = getShortestPath(graph, start, end)
  originalTime = getFastestTime(graph, start, end)

  cheatingTimes = []
  for cheatingGraph in getCheatingOptions(graph, originalShortestPath):
    cheatingTime = getFastestTime(cheatingGraph, start, end)
    if cheatingTime < originalTime:
      cheatingTimes.append(originalTime - cheatingTime)

  cheatingTimesCount = dict(Counter(cheatingTimes))
  if cheatingTimesCount != expectations:
    print(f"❌ Fastest time didn't match. Expected:\n{expectations}\nActual:\n{cheatingTimesCount}")

_testCheats(sample, {
  2: 14,
  4: 14,
  6: 2,
  8: 4,
  10: 2,
  12: 3,
  20: 1,
  36: 1,
  38: 1,
  40: 1,
  64: 1,
})
