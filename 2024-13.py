from collections import namedtuple
from itertools import product
import re
from string import Template
from termcolor import colored

MAX_BUTTON_PRESSES = 100
COST = {
  'a': 3,
  'b': 1
}
Machine = namedtuple('Machine', 'a b prize', defaults=[0j,0j,0j])

def main(input):
  machines = []
  totalMinCost = 0

  btnRegexTemplate = Template('Button $btn: X\+(?P<real>\d+), Y\+(?P<imag>\d+)')
  aRegex = re.compile(btnRegexTemplate.substitute(btn='A'))
  bRegex = re.compile(btnRegexTemplate.substitute(btn='B'))
  prizeRegex = re.compile('Prize: X=(?P<real>\d+), Y=(?P<imag>\d+)')

  for machinesRaw in input.split('\n\n'):
    aDict = aRegex.search(machinesRaw).groupdict()
    bDict = bRegex.search(machinesRaw).groupdict()
    prizeDict = prizeRegex.search(machinesRaw).groupdict()
    machines.append(Machine(
      a=complex(int(aDict['real']), int(aDict['imag'])),
      b=complex(int(bDict['real']), int(bDict['imag'])),
      prize=complex(int(prizeDict['real']), int(prizeDict['imag'])),
    ))

  for machine in machines:
    maxA = getMaxReasonablePresses(machine.a, machine.prize)
    maxB = getMaxReasonablePresses(machine.b, machine.prize)

    if maxA == 0 and maxB == 0:
      continue

    aPositions = [machine.a * presses for presses in reversed(range(0, maxA))]
    bPositions = [machine.b * presses for presses in reversed(range(0, maxB))]

    costs = []
    for combination in product(aPositions, bPositions):
      aPressed = combination[0].real / machine.a.real
      bPressed = combination[1].real / machine.b.real

      arrivedAt = combination[0] + combination[1]
      if machine.prize == arrivedAt:
        aPressed = combination[0].real / machine.a.real
        bPressed = combination[1].real / machine.b.real
        gameCost = COST['a'] * aPressed + COST['b'] * bPressed
        costs.append(gameCost)

    totalMinCost += round(min(costs)) if len(costs) > 0 else 0

  return totalMinCost

def getMaxReasonablePresses(button, prize):
  maxPress = complex(prize.real / button.real, prize.imag / button.imag)
  return max(
    round(maxPress.real if maxPress.real <= MAX_BUTTON_PRESSES else 0),
    round(maxPress.imag if maxPress.imag <= MAX_BUTTON_PRESSES else 0),
  )

sample = '''
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
'''.strip()

print('Sample:', colored(main(sample), 'green'))
