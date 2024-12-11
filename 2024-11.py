from yaml import load, SafeLoader

UNCHANGED_STONE_MULTIPLIER = 2024

def buildStones(input):
  return list(map(int, input.split(' ')))

def main(input, blinks):
  stones = buildStones(input)
  changedStones = blink(stones, blinks)
  return len(changedStones)

def blink(stones, blinks):
  currentStones = stones
  for blink in reversed(range(1, blinks + 1)):
    changedStones = []
    for stone in currentStones:
      if stone == 0:
        changedStones.append(1)
        continue
      
      digits = len('%i' % stone)
      if not digits & 1:
        # Fastest way to get number of digits in the number https://stackoverflow.com/a/54054183
        # Algorithmic way to split number by digits https://www.reddit.com/r/learnpython/comments/10iw55k/comment/j5ien9m
        halfLen = digits // 2
        halfLenDivider = 10 ** halfLen
        changedStones.append(stone // halfLenDivider)
        changedStones.append(stone % halfLenDivider)
        continue

      changedStones.append(stone * UNCHANGED_STONE_MULTIPLIER)
    currentStones = changedStones
  return currentStones

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
print('Second challenge:', main(challengeInput, blinks=75))
