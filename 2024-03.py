import re

def main(memory):
  factorsRegex = re.compile('mul\((?P<multiplicand>\d+),(?P<multiplier>\d+)\)')

  output = 0
  for match in factorsRegex.finditer(memory):
    multiplication = match.groupdict()
    multiplicand = int(multiplication['multiplicand'])
    multiplier = int(multiplication['multiplier'])
    output += multiplicand * multiplier

  return output

memorySample = '''
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
'''.strip()

with open('2024-03-input.txt') as f:
    memoryFirstChallenge = f.read()

print("Sample:", main(memorySample))
print("First challenge:", main(memoryFirstChallenge))
