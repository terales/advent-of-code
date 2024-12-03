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

def conditionalMain(memory):
  conditionalsRegex = re.compile("(do\(\)|don't\(\))")
  conditionals = re.split(conditionalsRegex, memory)

  output = 0
  multiplicationsEnabled = True

  for step in conditionals:
    if step == 'do()':
      multiplicationsEnabled = True
    elif step == "don't()":
      multiplicationsEnabled = False
    elif multiplicationsEnabled:
      output += main(step)

  return output

memorySample = '''
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
'''.strip()

with open('2024-03-input.txt') as f:
    memoryChallenge = f.read()

memorySecondSample = '''
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
'''.strip()

print("Sample:", main(memorySample))
print("First challenge:", main(memoryChallenge))
print("Second sample:", conditionalMain(memorySecondSample))
print("Second challenge:", conditionalMain(memoryChallenge))
