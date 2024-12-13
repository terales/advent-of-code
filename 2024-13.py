from collections import namedtuple
from itertools import product
from string import Template
import re
from termcolor import colored

Machine = namedtuple('Machine', 'a b prize', defaults=[0j,0j,0j])
FIRST_CHALLENGE_MAX_BUTTON_PRESSES = 100
SECOND_CHALLENGE_PRIZE_INCREASE = 10000000000000
COST = {
  'a': 3,
  'b': 1,
}

def firstChallenge(input):
  machines = buildMachines(input)
  totalMinCost = 0

  for machine in machines:
    costs = []
    aPositions = [machine.a * presses for presses in reversed(range(0, FIRST_CHALLENGE_MAX_BUTTON_PRESSES + 1))]
    bPositions = [machine.b * presses for presses in reversed(range(0, FIRST_CHALLENGE_MAX_BUTTON_PRESSES + 1))]
      
    for a, b in product(aPositions, bPositions):
      arrivedAt = a + b
      if machine.prize == arrivedAt:
        aPressed = a.real / machine.a.real
        bPressed = b.real / machine.b.real
        costs.append(calcCost(aPressed, bPressed))
    
    totalMinCost += round(min(costs)) if len(costs) > 0 else 0
  return totalMinCost

def secondChallenge(input):
  machines = buildMachines(input, SECOND_CHALLENGE_PRIZE_INCREASE)
  totalMinCost = 0

  for machine in machines:
    bDividend = machine.prize.real * machine.a.imag - machine.a.real * machine.prize.imag
    bDivisor = machine.a.real * machine.b.imag - machine.b.real * machine.a.imag
    bPressed = round(abs(bDividend / bDivisor)) if bDivisor != 0 else 0

    aDividend = machine.prize.real - machine.prize.imag - (machine.b.real - machine.b.imag) * bPressed
    aDivisor = machine.a.real - machine.a.imag
    aPressed = round(abs(aDividend / aDivisor)) if aDivisor != 0 else 0

    arrivedAt = machine.a * aPressed + machine.b * bPressed

    if machine.prize == arrivedAt:
      totalMinCost += COST['a'] * aPressed + COST['b'] * bPressed
  return totalMinCost

def calcCost(aPressed, bPressed):
  return COST['a'] * aPressed + COST['b'] * bPressed

def buildMachines(text, increasePrizePositionBy=0):
  machines = []

  btnRegexTemplate = Template('Button $btn: X\+(?P<real>\d+), Y\+(?P<imag>\d+)')
  aRegex = re.compile(btnRegexTemplate.substitute(btn='A'))
  bRegex = re.compile(btnRegexTemplate.substitute(btn='B'))
  prizeRegex = re.compile('Prize: X=(?P<real>\d+), Y=(?P<imag>\d+)')

  for machinesRaw in text.split('\n\n'):
    aDict = aRegex.search(machinesRaw).groupdict()
    bDict = bRegex.search(machinesRaw).groupdict()
    prizeDict = prizeRegex.search(machinesRaw).groupdict()
    machines.append(Machine(
      a=complex(int(aDict['real']), int(aDict['imag'])),
      b=complex(int(bDict['real']), int(bDict['imag'])),
      prize=complex(int(prizeDict['real']) + increasePrizePositionBy, int(prizeDict['imag']) + increasePrizePositionBy),
    ))
  return machines

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

with open('2024-13-input.txt') as f:
  challengeInput = f.read().strip()

print('First challenge sample:', colored(firstChallenge(sample), 'green'))
print('First challenge:', colored(firstChallenge(challengeInput), 'green'))
print('Second challenge:', colored(secondChallenge(challengeInput), 'green'))
