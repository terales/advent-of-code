from collections import Counter
from copy import deepcopy
from math import inf
import time
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
NICE_CHEAT_TRESHOLD = 100

def main(input, cheatTreshold):
  map, start, end = buildMap(input)
  graph = buildGraph(map)
  originalShortestPath = getShortestPath(graph, start, end)
  originalTime = len(originalShortestPath)

  cheatingTimes = 0
  for stepBeforeCheat, stepsAfterCheat in getCheatingOptions(graph, originalShortestPath):
    cheatingTimes += calcCheatingGains(
      originalShortestPath,
      stepBeforeCheat,
      stepsAfterCheat,
      originalTime,
      cheatTreshold
    )

  return cheatingTimes

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

def getPathTime(graph, path):
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
      yield position, validNextSteps

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

def calcCheatingGains(originalPath, stepBeforeCheat, stepsAfterCheat, originalTime, cheatTreshold):
  cheatingTimes = 0
  indexBeforeCheat = originalPath.index(stepBeforeCheat)

  for stepAfterCheat in stepsAfterCheat:
    indexAfterCheat = originalPath.index(stepAfterCheat)

    cheatingTime = len(originalPath[:indexBeforeCheat + 1])
    cheatingTime += 1
    cheatingTime += len(originalPath[indexAfterCheat:])

    timeSaved = originalTime - cheatingTime
    if timeSaved >= cheatTreshold:
      cheatingTimes += 1
  return cheatingTimes

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
  shortestPath = getShortestPath(graph, start, end)
  time = getPathTime(graph, shortestPath)
  if time != expected:
    print(f"❌ Fastest time didn't match. Expected: {expected}, actual: {time}")

_testGetFastestTime(sample, 84)


def _testSample(input, cheatTreshold, expected):
  time = main(input, cheatTreshold)
  if time != expected:
    print(f"❌ Final sample test didn't pass. Expected: {expected}, actual: {time}")

_testSample(sample, 20, 5)


with open('2024-20-input.txt') as f:
  challengeInput = f.read().strip()

print('Starting first challenge', flush=True)
startTime = time.time()
answer = main(challengeInput, NICE_CHEAT_TRESHOLD)
secondsToCalculate = time.time() - startTime
print(f'First challenge: {answer}.\nTook {round(secondsToCalculate, 3)} seconds to calculate')
