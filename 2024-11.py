from yaml import load, SafeLoader

UNCHANGED_STONE_MULTIPLIER = 2024

def buildStones(input):
  return list(map(int, input.split(' ')))

def main(input, blinks):
  stones = buildStones(input)
  changedStones = blink(stones, blinks)
  return len(changedStones)

def blink(stones, blinks):
  if blinks <= 0:
    return stones
  
  changedStones = []

  for stone in stones:
    if stone == 0:
      changedStones.append(1)
      continue

    strStone = str(stone)
    lenStone = len(strStone)
    if lenStone % 2 == 0:
      halfLen = int(lenStone / 2)
      changedStones.append(int(strStone[:halfLen]))
      changedStones.append(int(strStone[halfLen:]))
      continue

    changedStones.append(stone * UNCHANGED_STONE_MULTIPLIER)
  
  return blink(changedStones, blinks - 1)

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

with open('2024-11-samples.yaml') as f:
  samples = load(f, Loader=SafeLoader)

for test in samples['stones']:
  actual = blink(buildStones(test['input']), test['blinks'])
  print(_test(test, ' '.join(map(str, actual))))

for test in samples['count']:
  actual = main(test['input'], test['blinks'])
  print(_test(test, actual))

with open('2024-11-input.txt') as f:
  challengeInput = f.read().strip()

print('First challenge:', main(challengeInput, blinks=25))