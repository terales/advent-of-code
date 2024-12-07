from collections import namedtuple
import operator
from itertools import product

OPERATORS_FISRT_CHALLENGE = [operator.add, operator.mul]
Equation = namedtuple('Equation', ['test', 'terms'])

def main(input, operators):
  equationsRaw = [line.split(' ') for line in input.split('\n')]
  
  equations = []
  for termsRaw in equationsRaw:
    equations.append(Equation(
      test = int(termsRaw[0].rstrip(':')),
      terms = [int(termRaw) for termRaw in termsRaw[1:]]
    ))

  return sum(getTruthfulTest(equation, operators) for equation in equations)

def getTruthfulTest(equation, operators):
  operations = len(equation.terms) - 1
  variants = product(operators, repeat=operations)

  for variant in variants:
    result = equation.terms[0]
    for operationIndex, operator in enumerate(variant):
      result = operator(result, equation.terms[operationIndex + 1])
    if result == equation.test:
      return equation.test
    
  return 0

def concatDigitsOperator(a, b):
  result = str(a) + str(b)
  return int(result)

sample = '''
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''.strip()

with open('2024-07-input.txt') as f:
    challengeInput = f.read()

print(main(sample, OPERATORS_FISRT_CHALLENGE))
print(main(challengeInput, OPERATORS_FISRT_CHALLENGE))
print(main(sample, OPERATORS_FISRT_CHALLENGE + [concatDigitsOperator]))
