from functools import cache
from yaml import load, SafeLoader

UNCHANGED_STONE_MULTIPLIER = 2024

def main(input, blinks):
  stones = list(map(int, input.split(' ')))
  stonesCount = 0
  for stone in stones:
    stonesCount += countStonesAfterBlink(stone, blinks)
  return stonesCount

@cache
def countStonesAfterBlink(stone, blinks):
  blinksLeft = blinks - 1
  if blinks <= 0:
    return 1

  if stone == 0:
    return countStonesAfterBlink(1, blinksLeft)
    
  digits = len('%i' % stone) # Fastest way to get number of digits in the number https://stackoverflow.com/a/54054183
  if digits % 2 == 0:
      # Algorithmic way to split number by digits https://www.reddit.com/r/learnpython/comments/10iw55k/comment/j5ien9m
      halfLen = digits // 2
      halfLenDivider = 10 ** halfLen
      leftStones = countStonesAfterBlink(stone // halfLenDivider, blinksLeft)
      rightStones = countStonesAfterBlink(stone % halfLenDivider, blinksLeft)
      return leftStones + rightStones

  return countStonesAfterBlink(stone * UNCHANGED_STONE_MULTIPLIER, blinksLeft)


with open('2024-11-samples.yaml') as f:
  samples = load(f, Loader=SafeLoader)

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

for test in samples:
  actual = main(test['input'], test['blinks'])
  print(_test(test, actual))


with open('2024-11-input.txt') as f:
  challengeInput = f.read().strip()


print('First challenge:', main(challengeInput, blinks=25))
print('Second challenge:', main(challengeInput, blinks=75))
