from collections import defaultdict

def main(input):
  rules, updates = [section.split('\n') for section in input.split('\n\n')]
  pageOrder = getPageOrder(rules)

  validUpdates = []
  invalidUpdates = []
  for update in updates:
    pagesUpdated = update.split(',')
    if isUpdateInValidOrder(pagesUpdated, pageOrder):
      validUpdates.append(pagesUpdated)
    else:
      invalidUpdates.append(pagesUpdated)

  fixedInvalidUpdates = [getFixedInvalidOrder(update, pageOrder) for update in invalidUpdates]

  validMiddlePages = [update[len(update)//2] for update in validUpdates]
  invalidMiddlePages = [update[len(update)//2] for update in fixedInvalidUpdates]

  return {
    'sum of valid updates': sum([int(page) for page in validMiddlePages]),
    'sum of invalid updates': sum([int(page) for page in invalidMiddlePages])
  }

def getPageOrder(rules):
  order = defaultdict(set)
  for rule in rules:
    former, latter = rule.split('|')
    order[former].add(latter)
  return order

def isUpdateInValidOrder(pagesUpdated, pageOrder):
  for pageIndex, page in enumerate(pagesUpdated):
    nextPageIndexes = getNextPageIndexes(page, pagesUpdated, pageOrder)
    if any([pageIndex > nextPageIndex for nextPageIndex in nextPageIndexes]):
      return False
  return True

def getFixedInvalidOrder(pagesUpdated, pageOrder):
  fixedUpdate = pagesUpdated.copy()
  for currentIndex, page in enumerate(pagesUpdated):
    nextPageIndexes = getNextPageIndexes(page, pagesUpdated, pageOrder)
    minIndex = min(nextPageIndexes) if len(nextPageIndexes) > 0 else len(pagesUpdated)
    if currentIndex > minIndex:
      fixedUpdate.remove(page)
      fixedUpdate.insert(minIndex, page)
      if isUpdateInValidOrder(fixedUpdate, pageOrder):
        return fixedUpdate
  
  return getFixedInvalidOrder(fixedUpdate, pageOrder)

def getNextPageIndexes(page, pagesUpdated, pageOrder):
  nextPages = pageOrder[page]
  nextPageIndexes = []
  for nextPage in nextPages:
    try:
      nextPageIndexes.append(pagesUpdated.index(nextPage))
    except ValueError:
      continue
  return nextPageIndexes

sample = '''
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''.strip()

with open('2024-05-input.txt') as f:
    firstChallengeInput = f.read()

print(main(sample))
print(main(firstChallengeInput))
